from sqlalchemy import (JSON, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

orders_poses = Table(
    'order_poses',
    Base.metadata,
    Column('orders_id', Integer, ForeignKey('orders.id')),
    Column('poses_id', Integer, ForeignKey('poses.id'))
)


class Orders(Base):
    """Main class definition"""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    fashion_model_id = Column(Integer, ForeignKey('fashion_models.id'))
    status = Column(String)

    fashion_models = relationship('FashionModels')
    order_poses = relationship('OrderPoses')
    users = relationship('Users')

    poses = relationship("Poses", secondary=orders_poses)


class Users(Base):
    """Main class definition"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)


class FashionModels(Base):
    """Main class definition"""
    __tablename__ = 'fashion_models'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tensors_file_url = Column(String)


class FashionModelImages(Base):
    """Main class definition"""
    __tablename__ = 'fashion_model_images'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    url = Column(String)
    info = Column(JSON)
    fashion_model_id = Column(Integer, ForeignKey('fashion_models.id'))

    fashion_models = relationship('FashionModels')


class Poses(Base):
    """Main class definition"""
    __tablename__ = 'poses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Orders", secondary=orders_poses)


class PosesImages(Base):
    """Main class definition"""
    __tablename__ = 'poses_images'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    url = Column(String)
    info = Column(JSON)
    poses_id = Column(Integer, ForeignKey('poses.id'))

    poses = relationship('Poses')


class OrderImages(Base):
    """Main class definition"""
    __tablename__ = 'order_images'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    url = Column(String)
    info = Column(JSON)
    order_id = Column(Integer, ForeignKey('orders.id'))

    orders = relationship('Orders')


class Results(Base):
    """Main class definition"""
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    info = Column(JSON)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))

    users = relationship('Users')
    orders = relationship('Orders')


class ResultImages(Base):
    """Main class definition"""
    __tablename__ = 'result_images'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    url = Column(String)
    info = Column(JSON)
    result_id = Column(Integer, ForeignKey('results.id'))

    results = relationship('Results')
