from app.schemas.common import MessageResponse, HealthResponse
from app.schemas.auth import UserRegister, UserLogin, UserResponse, Token
from app.schemas.patient import PatientCreate, PatientResponse, AdmissionResponse, AppointmentResponse
from app.schemas.department import DepartmentResponse, BedResponse
from app.schemas.dashboard import KPISummary, RevenueInsights, DepartmentList, AlertList, AIInsights
from app.schemas.predictive import ForecastResponse, MedicineForecastItem, InventoryForecastItem, PredictiveSummaryResponse
from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse, ConversationCreate, ConversationResponse
from app.schemas.inventory import InventoryItemCreate, InventoryItemResponse, InventoryStatusResponse, LowStockItemResponse, ExpiryAlertResponse
from app.schemas.procurement import VendorResponse, VendorAnalysisResponse, PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse, AIProcurementRecommendation
from app.schemas.report import ReportGenerateRequest, ReportResponse, ReportHistoryItem

__all__ = [
    "MessageResponse", "HealthResponse",
    "UserRegister", "UserLogin", "UserResponse", "Token",
    "PatientCreate", "PatientResponse", "AdmissionResponse", "AppointmentResponse",
    "DepartmentResponse", "BedResponse",
    "KPISummary", "RevenueInsights", "DepartmentList", "AlertList", "AIInsights",
    "ForecastResponse", "MedicineForecastItem", "InventoryForecastItem", "PredictiveSummaryResponse",
    "ChatMessageRequest", "ChatMessageResponse", "ConversationCreate", "ConversationResponse",
    "InventoryItemCreate", "InventoryItemResponse", "InventoryStatusResponse", "LowStockItemResponse", "ExpiryAlertResponse",
    "VendorResponse", "VendorAnalysisResponse", "PurchaseOrderCreate", "PurchaseOrderUpdate", "PurchaseOrderResponse", "AIProcurementRecommendation",
    "ReportGenerateRequest", "ReportResponse", "ReportHistoryItem"
]
