from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from app.models import Vendor, PurchaseOrder, PurchaseOrderItem, InventoryItem
from app.schemas.procurement import (
    VendorCreate, VendorResponse, VendorAnalysisResponse,
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse,
    AIProcurementRecommendation
)
from app.services.inventory.inventory_service import InventoryService
from app.services.ai.factory import get_ai_provider

class ProcurementService:
    @staticmethod
    def get_vendors(db: Session) -> List[VendorAnalysisResponse]:
        vendors = db.query(Vendor).all()
        result = []
        for v in vendors:
            active_pos = db.query(func.count(PurchaseOrder.id)).filter(
                PurchaseOrder.vendor_id == v.id,
                PurchaseOrder.status.in_(["Draft", "Pending", "Approved", "Ordered"])
            ).scalar() or 0

            result.append(VendorAnalysisResponse(
                id=v.id,
                name=v.name,
                contact_person=v.contact_person,
                email=v.email,
                phone=v.phone,
                address=v.address,
                average_delivery_days=v.average_delivery_days or 5,
                reliability_score=v.reliability_score or 100.0,
                rating=v.rating or 5.0,
                active_purchase_orders_count=active_pos
            ))
        return result

    @staticmethod
    def create_vendor(db: Session, vendor_in: VendorCreate) -> Vendor:
        v = Vendor(**vendor_in.model_dump())
        db.add(v)
        db.commit()
        db.refresh(v)
        return v


    @staticmethod
    def create_purchase_order(db: Session, po_in: PurchaseOrderCreate) -> PurchaseOrder:
        vendor = db.query(Vendor).filter(Vendor.id == po_in.vendor_id).first()
        if not vendor:
            raise ValueError("Vendor not found")

        po = PurchaseOrder(
            vendor_id=po_in.vendor_id,
            status=po_in.status,
            total_amount=po_in.total_amount,
            expected_delivery_date=po_in.expected_delivery_date
        )
        db.add(po)
        db.commit()
        db.refresh(po)

        for item in po_in.items:
            po_item = PurchaseOrderItem(
                purchase_order_id=po.id,
                inventory_item_id=item.inventory_item_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            )
            db.add(po_item)

        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def list_purchase_orders(db: Session) -> List[PurchaseOrder]:
        return db.query(PurchaseOrder).all()

    @staticmethod
    def get_purchase_order(db: Session, po_id: int) -> Optional[PurchaseOrder]:
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()

    @staticmethod
    def update_purchase_order_status(db: Session, po_id: int, update: PurchaseOrderUpdate) -> PurchaseOrder:
        valid_statuses = ["Draft", "Pending", "Approved", "Ordered", "Received", "Cancelled"]
        if update.status not in valid_statuses:
            raise ValueError(f"Invalid status: {update.status}")

        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
        if not po:
            raise ValueError("Purchase order not found")

        po.status = update.status
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    async def get_ai_recommendations(db: Session) -> AIProcurementRecommendation:
        low_stock = InventoryService.get_low_stock(db)
        vendors = db.query(Vendor).all()

        suggested = []
        for item in low_stock:
            v = vendors[0] if vendors else None
            suggested.append({
                "inventory_item_id": item.id,
                "item_name": item.name,
                "recommended_quantity": item.reorder_recommended_qty,
                "preferred_vendor_id": v.id if v else 1,
                "preferred_vendor_name": v.name if v else "Primary Vendor",
                "estimated_cost": round(item.reorder_recommended_qty * 1.5, 2)
            })

        return AIProcurementRecommendation(
            summary=f"Automated procurement engine evaluated inventory levels. {len(suggested)} reorder proposals generated.",
            suggested_orders=suggested,
            cost_optimization_tips=[
                "Consolidate orders with primary vendors to negotiate bulk volume discounts.",
                "Review expiry dates before placing large replenishment orders."
            ]
        )
