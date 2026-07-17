"""Configuration settings for ASTMS application."""

class Config:
    """Base configuration class containing application variables."""
    APPLICATION_NAME = "Ahmedabad Smart Traffic Signal Management System"
    PROJECT_NAME = "ASTMS"
    SECRET_KEY = "astms_super_secret_key_for_development"
    DEBUG = True
    APPLICATION_VERSION = "1.0.0"
    
    # Dummy Login Credentials (as per requirements)
    DUMMY_USERNAME = "admin"
    DUMMY_PASSWORD = "admin123"
