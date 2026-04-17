from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

# 1. User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)  # Повертаємо це
    password = Column(String, nullable=False)  # І це
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    posts = relationship("Post", back_populates="author")

# 2. Profile (One-to-One з User)
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(Text)
    avatar_url = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    user = relationship("User", back_populates="profile")

# 3. Category (One-to-Many з Post)
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    
    posts = relationship("Post", back_populates="category")

# 4. Post (Many-to-One до User та Category)
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

# 5. Comment (Many-to-One до Post)
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    post = relationship("Post", back_populates="comments")