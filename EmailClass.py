from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Dict
import json

class SentimentLevel(str, Enum):
    """
    Classifies the emotional tone of the email content.
    Used for prioritizing responses and tracking customer satisfaction.
    """
    VERY_POSITIVE = "very_positive"  # Extremely satisfied, enthusiastic
    POSITIVE = "positive"  # Generally happy, content
    NEUTRAL = "neutral"  # Neither positive nor negative
    NEGATIVE = "negative"  # Dissatisfied, unhappy
    VERY_NEGATIVE = "very_negative"  # Extremely dissatisfied, angry

class UrgencyLevel(str, Enum):
    """
    Indicates how quickly the email needs to be addressed.
    Critical for response prioritization and resource allocation.
    """
    STANDARD = "standard"  # Normal processing time acceptable
    URGENT = "urgent"  # Requires faster than normal response
    IMMEDIATE = "immediate"  # Needs immediate attention
    EMERGENCY = "emergency"  # Critical situation requiring instant response

class PurposeType(str, Enum):
    """
    Classifies the primary purpose of the email communication.
    Used to route emails to appropriate departments and track communication patterns.
    """
    BOOKING_INQUIRY = "booking_inquiry"  # New bookings or booking-related questions
    CUSTOMER_SUPPORT = "customer_support"  # Support requests and assistance
    FEEDBACK = "feedback"  # Reviews, complaints, and testimonials
    PARTNERSHIP = "partnership"  # Business partnership inquiries
    MARKETING = "marketing"  # Marketing-related communications
    OTHER = "other"  # Uncategorized communications

class BookingType(str, Enum):
    """
    Specifies the type of booking-related inquiry.
    Helps in prioritizing and routing booking requests to specialized teams.
    """
    NEW_RESERVATION = "new_reservation"  # First-time bookings
    MODIFICATION = "modification"  # Changes to existing bookings
    CANCELLATION = "cancellation"  # Booking cancellation requests
    PRICE_CHECK = "price_check"  # Pricing inquiries
    GROUP_BOOKING = "group_booking"  # Bookings for groups
    CORPORATE_BOOKING = "corporate_booking"  # Business travel bookings

class SupportType(str, Enum):
    """
    Categorizes the type of support being requested.
    Used for support ticket routing and response prioritization.
    """
    DOCUMENTATION = "documentation"  # Travel document assistance
    LUGGAGE = "luggage"  # Lost/delayed baggage issues
    TRANSFER = "transfer"  # Transportation arrangements
    CHECK_IN = "check_in"  # Check-in assistance
    INSURANCE = "insurance"  # Travel insurance queries
    VISA_ASSISTANCE = "visa_assistance"  # Visa-related help
    MEDICAL = "medical"  # Health-related concerns
    SAFETY = "safety"  # Safety/security concerns
    COMPLAINT = "complaint"  # Customer complaints
    OTHER = "other"  # Miscellaneous support requests

class TravelType(str, Enum):
    """
    Identifies the purpose or style of travel being discussed.
    Helps in tailoring responses and recommendations.
    """
    LEISURE = "leisure"  # Vacation/recreational travel
    BUSINESS = "business"  # Corporate travel
    HONEYMOON = "honeymoon"  # Wedding/honeymoon travel
    FAMILY = "family"  # Family-oriented trips
    ADVENTURE = "adventure"  # Adventure/activity-focused travel
    LUXURY = "luxury"  # High-end luxury travel
    EDUCATIONAL = "educational"  # Study/learning-focused travel
    MEDICAL = "medical"  # Healthcare-related travel

class ServiceMentioned(BaseModel):
    """
    Tracks which travel services are mentioned in the email.
    Used for service demand analysis and cross-selling opportunities.
    
    Attributes:
        flights (bool): Mentions of air travel
        hotels (bool): Accommodation references
        car_rental (bool): Vehicle rental inquiries
        tours (bool): Guided tour mentions
        insurance (bool): Travel insurance discussions
        visa_services (bool): Visa assistance mentions
        transfers (bool): Transport service references
        activities (bool): Activity/excursion mentions
    """
    flights: bool 
    hotels: bool 
    car_rental: bool 
    tours: bool 
    insurance: bool 
    visa_services: bool 
    transfers: bool 
    activities: bool 

class MonetaryReference(BaseModel):
    """
    Analyzes financial aspects mentioned in the email.
    Useful for budget analysis and price sensitivity tracking.
    
    Attributes:
        currency: Type of currency mentioned
        mentioned_amount: Specific amount referenced
        price_sensitivity: Customer's sensitivity to pricing (0-1)
        budget_category: Luxury/mid-range/budget classification
        payment_method_mentioned: Referenced payment methods
    """
    currency: str
    mentioned_amount: float
    price_sensitivity: float
    #budget_category: str]
    #payment_method_mentioned: str]

class TripDetails(BaseModel):
    """
    Captures specific details about the trip being discussed.
    Essential for understanding customer requirements and preferences.
    
    Attributes:
        destination: Primary travel destination
        alternative_destinations: Other locations considered
        travel_dates: Planned travel dates
        flexibility: Date flexibility indicator
        group_size: Number of travelers
        duration: Length of trip in days
        travel_type: Purpose/style of travel
        special_requirements: Specific needs or requests
        activities_interested: Desired activities/experiences
        dietary_requirements: Food preferences/restrictions
        accessibility_needs: Accessibility requirements
    """
    destination: str
    alternative_destinations: List[str]
    travel_dates: List[str]
    flexibility: bool
    group_size: int
    duration: int
    travel_type: TravelType
    budget_range: str
    special_requirements: List[str]
    #accommodation_preference: str]
    #transportation_preference: str]
    #activities_interested: List[str]]
    #dietary_requirements: List[str]]
    accessibility_needs: List[str]

class SentimentAnalysis(BaseModel):
    """
    Analyzes the emotional content and urgency of the email.
    Critical for prioritizing responses and identifying customer satisfaction issues.
    
    Attributes:
        overall_tone: General sentiment of the message
        urgency: Level of urgency expressed
        satisfaction_score: Customer satisfaction indicator (0-1)
        emotional_indicators: Detected emotional expressions
        key_phrases: Important phrases identified
        complaint_indicators: Signs of dissatisfaction
        praise_indicators: Positive feedback markers
        frustration_level: Detected frustration (0-1)
        response_expectation: Expected response timeframe
    """
    overall_tone: SentimentLevel
    urgency: UrgencyLevel
    satisfaction_score: float
    #emotional_indicators: List[str]
    #key_phrases: List[str]]
    #complaint_indicators: List[str]]
    #praise_indicators: List[str]]
    #frustration_level: float]
    #response_expectation: str]

# 

class CompetitorMention(BaseModel):
    """
    Tracks and analyzes mentions of competitor services.
    Valuable for competitive analysis and service improvement.
    
    Attributes:
        competitor_name: Name of mentioned competitor
        context: Context of the mention
        sentiment: Sentiment towards competitor
        price_comparison: Price comparison indicator
        service_comparison: Service comparison indicator
    """
    competitor_name: str
    context: str
    sentiment: SentimentLevel
    price_comparison: bool
    service_comparison: bool

# CUSTOMER ANALYSIS REQUIRES CRM OR DB CONNEXION, MIGHT BE INTERESTING TO 
# IMPLEMENT IN REAL LIFE BUT OUTSIDE OF SCOPE

# class CustomerStatus(str, Enum):
#     """
#     Categorizes the customer's relationship with the agency.
#     Used for service level determination and priority handling.
#     """
#     NEW = "new"  # First-time customer
#     RETURNING = "returning"  # Repeat customer
#     VIP = "vip"  # High-value customer
#     CORPORATE = "corporate"  # Business account
#     INFLUENCER = "influencer"  # Social media influencer/partner
# class CustomerContext(BaseModel):
#     """
#     Provides comprehensive customer background information.
#     Used for personalized service and customer relationship management.
    
#     Attributes:
#         status: Customer loyalty level
#         email: Contact email address
#         language_preference: Preferred communication language
#         previous_interactions_count: Number of past interactions
#         lifetime_value: Total customer spend
#         loyalty_points: Accumulated reward points
#         preferred_contact_method: Preferred communication channel
#         social_media_presence: Social media profiles
#         marketing_preferences: Marketing opt-in status
#         frequent_destinations: Common travel locations
#         complaint_history: Past complaint records
#         preferred_airlines: Airline preferences
#         preferred_hotel_chains: Hotel chain preferences
#     """
#     status: CustomerStatus
#     email: str
#     language_preference: str]
#     previous_interactions_count: int]
#     last_interaction_date: str]
#     lifetime_value: float]
#     loyalty_points: int]
#     preferred_contact_method: str]
#     social_media_presence: Dict[str, str]]
#     marketing_preferences: Dict[str, bool]]
#     frequent_destinations: List[str]]
#     complaint_history: List[str]]
#     preferred_airlines: List[str]]
#     preferred_hotel_chains: List[str]]

class EmailAnalysis(BaseModel):
    """
    Main class for comprehensive email analysis.
    Combines all aspects of email analysis for customer service and business intelligence.
    
    Key Components:
    - Basic email metadata (ID, timestamp, subject)
    - Purpose and type classification
    - Content analysis (services, monetary aspects, competitors)
    - Sentiment analysis
    - Trip details
    - Customer context
    - Priority and routing information
    - Compliance and legal considerations
    - Processing metadata and AI analysis results
    
    Used for:
    1. Customer service optimization
    2. Business intelligence gathering
    3. Service quality monitoring
    4. Compliance tracking
    5. Performance analytics
    """
    # Basic Email Information
    email_id: str
    subject: str
    sender_email: str
    recipient_email: List[str]
    #thread_id: str]
    #response_to: str]
    
    # Purpose Classification
    primary_purpose: PurposeType
    secondary_purposes: List[PurposeType] 
    booking_type: BookingType
    support_type: SupportType
    
    # Content Analysis
    #word_count: int
    language_detected: str
    services_mentioned: ServiceMentioned
    monetary_references: MonetaryReference
    competitor_mentions: List[CompetitorMention]
    # urls_mentioned: List[str]]
    # attachments: List[str]]
    
    # Sentiment Analysis
    sentiment: SentimentAnalysis
    
    # Trip Information
    trip_details: TripDetails
    
    # Customer Information
    # customer_context: CustomerContext
    
    # Priority and Routing
    priority_score: float
    #suggested_department: str]
    #estimated_response_time: int]
    #auto_reply_sent: bool 
    
    # Compliance and Legal
    contains_sensitive_data: bool 
    gdpr_relevant: bool 
    #requires_legal_review: bool 
    
    # Additional Metadata
    #tags: List[str] = []
    requires_immediate_attention: bool 
    # processed_by: str]
    # processing_time: float]
    confidence_score: float
    # notes: str]
    follow_up_required: bool 
    #follow_up_date: str]
    
    # AI Processing Metadata
    #ai_confidence_scores: Dict[str, float]
    #classification_version: str]

# Dump schema into json file
# with open("EmailAnalysisSchema.json", "w") as json_file:
#     json.dump(json.loads(EmailAnalysis.schema_json()), json_file, indent=4)