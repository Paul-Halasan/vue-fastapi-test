from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
import pandas as pd

# Helper function to cap profit margin within database limits
def cap_profit_margin(margin_value):
    """Cap profit margin to fit DECIMAL(8,2) database constraint (-999999.99 to 999999.99)"""
    return max(min(float(margin_value), 999999.99), -999999.99)

# Helper function to calculate profit margin safely
def calculate_profit_margin(selling_price, total_cost):
    """Calculate profit margin with proper capping"""
    if total_cost == 0:
        return 0.00
    margin = ((float(selling_price) - float(total_cost)) / float(total_cost)) * 100
    return cap_profit_margin(margin)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency - para may DB session sa bawat request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://vue-fastapi-test.vercel.app/"],
    # allow_origins=[
    #     "http://localhost:5173",  # Vite dev (local)
    #     "https://vue-fastapi-test.vercel.app",  # Vercel deployment
    #     "https://vue-fastapi-test-mt8rny0qo-paul-halasans-projects.vercel.app"
    # ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
  return {"ok": True}

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

# GET all products
@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# POST new product
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    print('create_product received:', product)

    existing_product = db.query(models.Product).filter(models.Product.product_name == product.product_name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
 
    # Step 1: Create the product first
    new_product = models.Product(
        product_name=product.product_name,
        total_cost=product.total_cost,
        suggested_price=product.total_cost * 3.3, #markup calculation
        selling_price=product.selling_price,
        profit=product.selling_price - product.total_cost,
        profit_margin=calculate_profit_margin(product.selling_price, product.total_cost),
    )

    # Step 2: Save product to database to get the product_id
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Now new_product.product_id is available!

    # Step 3: Create product-material relationships using the new product_id
    for each in product.materials:
        print('Material in product.materials:', each)

        # Verify that the material exists
        material = db.query(models.Material).filter(models.Material.material_id == each.material_id).first()
        if not material:
            raise HTTPException(status_code=404, detail=f"Material with ID {each.material_id} not found")

        new_product_material = models.ProductMaterial(
            product_id = new_product.product_id,  # Now this exists!
            material_id = each.material_id,
            quantity_used = each.quantity_used
        )
        
        # Actually save the product-material relationship
        db.add(new_product_material)

    # Step 4: Commit all product-material relationships
    db.commit()
    
    return new_product

# PATCH update product (name and/or selling_price)
@app.patch("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_product = db.query(models.Product).filter(
        models.Product.product_name == update.product_name,
        models.Product.product_id != product_id
    ).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    
    update_data = update.model_dump(exclude_unset=True)  # ← magic: only keeps fields provided by user
    
    for key, value in update_data.items():
        setattr(product, key, value)

    if product.selling_price <= product.total_cost:
        raise HTTPException(status_code=400, detail="Selling price cannot be lower or equal to total cost")

    db.commit()
    db.refresh(product)
    return product

# DELETE product by ID
@app.delete("/products/{product_id}", response_model=schemas.ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product



# GET all materials
@app.get("/materials", response_model=list[schemas.MaterialResponse])
def get_materials(db: Session = Depends(get_db)):
    materials = db.query(models.Material).all()
    return materials

# POST new material
@app.post("/materials", response_model=schemas.MaterialResponse)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    existing_material = db.query(models.Material).filter(models.Material.material_name == material.material_name).first()
    if existing_material:
        raise HTTPException(status_code=400, detail="Material with this name already exists")

    new_material = models.Material(
        material_name = material.material_name,
        material_type = material.material_type,
        material_unit = material.material_unit,
        material_price = material.material_price,
        material_quantity = material.material_quantity,
        material_unit_price = material.material_price/material.material_quantity,
        material_supplier = material.material_supplier
    )

    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

# PATCH update material (name/type/unit/price/quantity/supplier)
@app.patch("/materials/{material_id}", response_model=schemas.MaterialResponse)
def update_material(material_id: int, update: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.material_id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    existing_material = db.query(models.Material).filter(
        models.Material.material_name == update.material_name,
        models.Material.material_id != material_id
    ).first()
    if existing_material:
        raise HTTPException(status_code=400, detail="Material with this name already exists")

    update_data = update.model_dump(exclude_unset=True)  # ← magic: only keeps fields provided by user
    
    for key, value in update_data.items():
        setattr(material, key, value)
    
    # Recompute unit_price kung nagbago price o quantity
    if "material_price" in update_data or "material_quantity" in update_data:
        if material.material_quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
        material.material_unit_price = material.material_price / material.material_quantity

    db.commit()
    db.refresh(material)

    #recompute affected products' total_cost, suggested_price, profit, profit_margin
    product_links = db.query(models.ProductMaterial).filter(models.ProductMaterial.material_id == material_id).all()
    if product_links:
        product_ids = [pl.product_id for pl in product_links]
        products = db.query(models.Product).filter(models.Product.product_id.in_(product_ids)).all()
        for product in products:
            # Recalculate total_cost based on all its materials
            total_cost = 0.0
            product_materials = db.query(models.ProductMaterial).filter(models.ProductMaterial.product_id == product.product_id).all()
            for pm in product_materials:
                mat = db.query(models.Material).filter(models.Material.material_id == pm.material_id).first()
                if mat:
                    total_cost += float(mat.material_unit_price) * float(pm.quantity_used)
            product.total_cost = total_cost
            product.suggested_price = total_cost * 3.3  # markup calculation
            product.profit = float(product.selling_price) - total_cost
            if total_cost > 0:
                product.profit_margin = calculate_profit_margin(product.selling_price, total_cost)
            else:
                product.profit_margin = 0.00
        db.commit()


    return material

# DELETE material by ID
@app.delete("/materials/{material_id}", response_model=schemas.MaterialResponse)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.material_id == material_id).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # Find products using this material
    product_links = db.query(models.ProductMaterial).filter(models.ProductMaterial.material_id == material_id).all()
    if product_links:
        product_ids = [pl.product_id for pl in product_links]
        products = db.query(models.Product).filter(models.Product.product_id.in_(product_ids)).all()
        product_names = [p.product_name for p in products]

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Cannot delete material because it is used in one or more products",
                "products_using_material": product_names
            }
        )
    
    db.delete(material)
    db.commit()
    return material


# GET all product-materials
@app.get("/product-materials", response_model=list[schemas.ProductMaterialResponse])
def get_product_materials(db: Session = Depends(get_db)):
    product_materials = db.query(models.ProductMaterial).all()
    return product_materials

# POST new product-material
@app.post("/product-materials", response_model=schemas.ProductMaterialResponse)
def create_product_material(pm: schemas.ProductMaterialCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == pm.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    material = db.query(models.Material).filter(models.Material.material_id == pm.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    if pm.quantity_used <= 0:
        raise HTTPException(status_code=400, detail="Quantity used must be greater than zero")

    new_pm = models.ProductMaterial(
        product_id = pm.product_id,
        material_id = pm.material_id,
        quantity_used = pm.quantity_used
    )

    # Recalculate product total_cost, suggested_price, profit, profit_margin
    additional_cost = float(material.material_unit_price) * pm.quantity_used
    product.total_cost += additional_cost
    product.suggested_price = product.total_cost * 3.3  # markup calculation
    product.profit = product.selling_price - product.total_cost
    if product.total_cost > 0:
        product.profit_margin = calculate_profit_margin(product.selling_price, product.total_cost)
    else:
        product.profit_margin = 0.00

    db.add(new_pm)
    db.commit()
    db.refresh(new_pm)
    return new_pm

# PATCH update product-material (quantity_used)
@app.patch("/product-materials/{pm_id}", response_model=schemas.ProductMaterialResponse)
def update_product_material(pm_id: int, update: schemas.ProductMaterialUpdate, db: Session = Depends(get_db)):
    pm = db.query(models.ProductMaterial).filter(models.ProductMaterial.pm_id == pm_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Product-Material entry not found")
    
    product = db.query(models.Product).filter(models.Product.product_id == pm.product_id).first()
    material = db.query(models.Material).filter(models.Material.material_id == pm.material_id).first()
    if not product or not material:
        raise HTTPException(status_code=404, detail="Associated Product or Material not found")
    
    if update.quantity_used is None or update.quantity_used <= 0:
        raise HTTPException(status_code=400, detail="Quantity used must be greater than zero")

    # Recalculate product total_cost, suggested_price, profit, profit_margin
    old_cost = float(material.material_unit_price) * float(pm.quantity_used)
    new_cost = float(material.material_unit_price) * float(update.quantity_used)
    cost_difference = new_cost - old_cost

    product.total_cost = float(product.total_cost) + float(cost_difference)
    product.suggested_price = float(product.total_cost) * 3.3  # markup calculation
    product.profit = float(product.selling_price) - float(product.total_cost)
    if float(product.total_cost) > 0:
        product.profit_margin = calculate_profit_margin(product.selling_price, product.total_cost)
    else:
        product.profit_margin = 0.00

    pm.quantity_used = update.quantity_used

    db.commit()
    db.refresh(pm)
    return pm

# DELETE product-material by ID
@app.delete("/product-materials/{pm_id}", response_model=schemas.ProductMaterialResponse)
def delete_product_material(pm_id: int, db: Session = Depends(get_db)):
    pm = db.query(models.ProductMaterial).filter(models.ProductMaterial.pm_id == pm_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Product-Material entry not found")
    
    product = db.query(models.Product).filter(models.Product.product_id == pm.product_id).first()
    material = db.query(models.Material).filter(models.Material.material_id == pm.material_id).first()
    if not product or not material:
        raise HTTPException(status_code=404, detail="Associated Product or Material not found")

    # Recalculate product total_cost, suggested_price, profit, profit_margin
    reduction_cost = float(material.material_unit_price) * float(pm.quantity_used)
    product.total_cost = float(product.total_cost) - reduction_cost
    product.suggested_price = product.total_cost * 3.3  # markup calculation
    product.profit = float(product.selling_price) - product.total_cost
    if product.total_cost > 0:
        product.profit_margin = calculate_profit_margin(product.selling_price, product.total_cost)
    else:
        product.profit_margin = 0.00

    db.delete(pm)
    db.commit()
    return pm

@app.post("/materials/import")
def import_materials(data: list[dict], db: Session = Depends(get_db)):
    try:
        # Iterate through the JSON data and add materials to the database

        print('Importing materials data:', data)

        for row in data:
            new_material = models.Material(
                material_name=row['material_name'],
                material_type=row['material_type'],
                material_unit=row['material_unit'],
                material_price=row['material_price'],
                material_quantity=row['material_quantity'],
                material_supplier=row['material_supplier'] if row['material_supplier'] else "n/a",
                material_unit_price=row['material_price'] / row['material_quantity']
            )
            db.add(new_material)

        db.commit()
        return {"message": "Materials imported successfully!"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to import materials: {str(e)}")