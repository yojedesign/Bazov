"""
Scrapy items for LinkedIn data
"""

import scrapy


class LinkedInProfileItem(scrapy.Item):
    """LinkedIn profile data"""
    
    # Basic information
    linkedin_id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    full_name = scrapy.Field()
    headline = scrapy.Field()
    
    # Profile URLs
    profile_url = scrapy.Field()
    avatar_url = scrapy.Field()
    
    # Current position
    current_title = scrapy.Field()
    current_company = scrapy.Field()
    current_company_id = scrapy.Field()
    
    # Location
    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    
    # About section
    about = scrapy.Field()
    
    # Experience
    experience = scrapy.Field()  # List of dicts
    
    # Education
    education = scrapy.Field()  # List of dicts
    
    # Skills
    skills = scrapy.Field()  # List of strings
    
    # Contact info
    email = scrapy.Field()
    phone = scrapy.Field()
    
    # Social links
    twitter_url = scrapy.Field()
    github_url = scrapy.Field()
    personal_website = scrapy.Field()
    
    # Connections
    connections_count = scrapy.Field()
    
    # Metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()


class LinkedInConnectionItem(scrapy.Item):
    """LinkedIn connection data"""
    
    # Profile IDs
    from_person_id = scrapy.Field()
    to_person_id = scrapy.Field()
    
    # Connection details
    relationship_type = scrapy.Field()  # e.g., "colleague", "classmate", "friend"
    connected_at = scrapy.Field()
    
    # Additional info
    notes = scrapy.Field()
    
    # Metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()


class LinkedInCompanyItem(scrapy.Item):
    """LinkedIn company data"""
    
    # Basic information
    linkedin_id = scrapy.Field()
    name = scrapy.Field()
    domain = scrapy.Field()
    
    # Profile URLs
    company_url = scrapy.Field()
    logo_url = scrapy.Field()
    website_url = scrapy.Field()
    
    # Industry and size
    industry = scrapy.Field()
    size = scrapy.Field()
    
    # Location
    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    address = scrapy.Field()
    
    # Description
    description = scrapy.Field()
    founded_year = scrapy.Field()
    
    # Employee count
    employee_count = scrapy.Field()
    
    # Metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()


class LinkedInJobItem(scrapy.Item):
    """LinkedIn job posting data"""
    
    # Job information
    job_id = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    company_id = scrapy.Field()
    location = scrapy.Field()
    
    # Job details
    description = scrapy.Field()
    requirements = scrapy.Field()
    benefits = scrapy.Field()
    
    # Employment type
    employment_type = scrapy.Field()  # Full-time, Part-time, Contract, etc.
    experience_level = scrapy.Field()  # Entry, Mid, Senior, etc.
    
    # Dates
    posted_at = scrapy.Field()
    expires_at = scrapy.Field()
    
    # URL
    job_url = scrapy.Field()
    
    # Metadata
    scraped_at = scrapy.Field()
    source_url = scrapy.Field()
