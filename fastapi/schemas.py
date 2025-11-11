from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

#PRODUCT SCHEMAS
class ProductBase(BaseModel):
    product_name: str
    selling_price: float

class ProductResponse(ProductBase):
    product_id: int
    product_name: str
    total_cost: float
    suggested_price: float
    profit: float
    profit_margin: float
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    selling_price: Optional[float] = None


#MATERIAL SCHEMAS
class MaterialBase(BaseModel):
    material_name: str
    material_type: str
    material_unit: str
    material_price: float
    material_quantity: int
    material_unit_price: float
    material_supplier: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    material_id: int
    material_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {"from_attributes": True}

class MaterialUpdate(BaseModel):
    material_name: Optional[str] = None
    material_type: Optional[str] = None
    material_unit: Optional[str] = None
    material_price: Optional[float] = None
    material_quantity: Optional[int] = None
    material_supplier: Optional[str] = None


# PRODUCT-MATERIAL SCHEMAS
class ProductMaterialBase(BaseModel):
    product_id: int
    material_id: int
    quantity_used: float

class ProductMaterialInput(BaseModel):
    material_id: int
    quantity_used: float

class ProductCreate(ProductBase):
    total_cost: float
    materials: List[ProductMaterialInput]

class ProductMaterialCreate(ProductMaterialBase):
    pass

class ProductMaterialResponse(ProductMaterialBase):
    pm_id: int
    product: ProductResponse
    material: MaterialResponse
    quantity_used: float

    class Config:
        model_config = {"from_attributes": True}

class ProductMaterialUpdate(BaseModel):
    quantity_used: float