from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    total_cost = Column(DECIMAL(10,2), nullable=False)
    suggested_price = Column(DECIMAL(10,2), nullable=False)
    selling_price = Column(DECIMAL(10,2), nullable=False)
    profit = Column(DECIMAL(10,2), nullable=False, default=0.00)
    profit_margin = Column(DECIMAL(8,2), nullable=False, default=0.00)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # relationship to product_materials
    materials = relationship("ProductMaterial", back_populates="product", cascade="all, delete")

class Material(Base):
    __tablename__ = "materials"

    material_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    material_name = Column(String(255), nullable=False)
    material_type = Column(String(255), nullable=False)
    material_unit = Column(String(255), nullable=False)
    material_price = Column(DECIMAL(10,2), nullable=False)
    material_quantity = Column(Integer, nullable=False)
    material_unit_price = Column(DECIMAL(10,2), nullable=False)
    material_supplier = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # relationship
    products = relationship("ProductMaterial", back_populates="material")

class ProductMaterial(Base):
    __tablename__ = "product_materials"

    pm_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.material_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    quantity_used = Column(DECIMAL(10,2), nullable=False)

    product = relationship("Product", back_populates="materials")
    material = relationship("Material", back_populates="products")
