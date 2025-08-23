from enum import Enum


class Status(Enum):
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"


class PaymentStatus(Enum):
    PENDING = "Pending"
    SUCCESSFUL = "Successful"
    REVERSED = "Reversed"
    FAILED = "Failed"


class Gender(Enum):
    MALE = "male"
    Female = "female"


class TemplateTier(Enum):
    PAID = "paid"
    FREE = "free"


class TemplateUnder(Enum):
    TEMPLATES = "templates"
    PRESENTATIONS = "presentations"


class TemplateCategory(Enum):
    PORTFOLIO = "portfolio"
    BUSINESS_CORPORATE = "business-corporate"
    ECOMMERCE = "e-commerce"
    EDUCATION = "education"
    HEALTH_FITNESS = "health-fitness"
    NON_PROFIT_CHARITY = "Non Profit & Charity"
    REAL_ESTATE = "real-estate"
    FINANCE = "finance"
    PERSONAL_DEVELOPMENT = "personal-development"
    INFOGRAPHICS = "infographics"








