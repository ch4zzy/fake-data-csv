from django.db import models


class DataType(models.TextChoices):
    """
    Enumeration class defining various data types and their display names.
    """

    FULL_NAME = "full_name", "Full Name"
    JOB = "job", "Job"
    EMAIL = "email", "Email"
    DOMAIN_NAME = "domain_name", "Domain Name"
    PHONE_NUMBER = "phone_number", "Phone Number"
    COMPANY_NAME = "company_name", "Company Name"
    TEXT = "text", "Text"
    INTEGER = "integer", "Integer"
    ADDRESS = "address", "Address"
    DATE = "date", "Date"


class Delimiter(models.TextChoices):
    """
    Enumeration class defining various delimiter options and their display names.
    """

    COMMA = ",", "Comma (,)"
    SEMICOLON = ";", "Semicolon (;)"
    TAB = "\t", "Tab (\t)"
    SPACE = " ", "Space ( )"
    VERTICAL_BAR = "|", "Vertical bar (|)"


class QuoteCharacter(models.TextChoices):
    """
    Enumeration class defining various quote character options and their display names.
    """

    DOUBLE_QUOTE = '"', 'Double-quote (")'
    SINGLE_QUOTE = "'", "Single-quote (')"


class Status(models.TextChoices):
    """
    Represents text-based choices for different status options.
    """

    READY = "Ready", "READY"
    PROCESSING = "Processing", "PROCESSING"
