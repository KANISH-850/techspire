import datetime
from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem
from app.models.vendor import Vendor
from app.models.purchase_order import PurchaseOrder

class InventoryAnalytics:
    @staticmethod
    def get_status(db: Session):
        total_items = db.query(InventoryItem).count()
        low_stock = db.query(InventoryItem).filter(InventoryItem.current_stock <= InventoryItem.minimum_stock).count()
        critical_stock = db.query(InventoryItem).filter(InventoryItem.current_stock <= InventoryItem.minimum_stock * 0.25).count()
        
        today = datetime.date.today()
        seven_days = today + datetime.timedelta(days=7)
        thirty_days = today + datetime.timedelta(days=30)
        
        expired = db.query(InventoryItem).filter(InventoryItem.expiry_date < today).count()
        expiring_soon = db.query(InventoryItem).filter(InventoryItem.expiry_date >= today, InventoryItem.expiry_date <= thirty_days).count()
        pending_pos = db.query(PurchaseOrder).filter(PurchaseOrder.status.in_(["Draft", "Pending", "Approved", "Ordered"])).count()
        
        return {
            "total_items": total_items,
            "low_stock": low_stock,
            "critical_stock": critical_stock,
            "expired": expired,
            "expiring_soon": expiring_soon,
            "pending_pos": pending_pos
        }

    @staticmethod
    def get_low_stock(db: Session):
        items = db.query(InventoryItem).filter(InventoryItem.current_stock <= InventoryItem.minimum_stock).all()
        results = []
        for item in items:
            priority = "Critical" if item.current_stock <= item.minimum_stock * 0.25 else "Low"
            vendor_name = db.query(Vendor).filter(Vendor.id == item.vendor_id).first().name if item.vendor_id else "Unknown"
            reorder_qty = item.maximum_stock - item.current_stock
            results.append({
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "current_stock": item.current_stock,
                "minimum_stock": item.minimum_stock,
                "maximum_stock": item.maximum_stock,
                "unit": item.unit,
                "vendor_id": item.vendor_id,
                "vendor_name": vendor_name,
                "priority": priority,
                "recommended_quantity": reorder_qty
            })
        return results

    @staticmethod
    def get_expiry_alerts(db: Session):
        items = db.query(InventoryItem).filter(InventoryItem.expiry_date != None).all()
        today = datetime.date.today()
        results = []
        for item in items:
            days_remaining = (item.expiry_date - today).days
            if days_remaining < 0:
                status = "Expired"
            elif days_remaining <= 7:
                status = "Expiring within 7 days"
            elif days_remaining <= 30:
                status = "Expiring within 30 days"
            else:
                continue # Safe
                
            results.append({
                "id": item.id,
                "name": item.name,
                "batch_number": item.batch_number,
                "expiry_date": item.expiry_date,
                "days_remaining": days_remaining,
                "current_stock": item.current_stock,
                "status": status
            })
        return results

    @staticmethod
    def get_vendor_analysis(db: Session):
        vendors = db.query(Vendor).all()
        results = []
        for v in vendors:
            supplied_items = db.query(InventoryItem).filter(InventoryItem.vendor_id == v.id).count()
            pos = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == v.id).all()
            total_value = sum(po.total_amount for po in pos)
            active_orders = len([po for po in pos if po.status in ["Draft", "Pending", "Approved", "Ordered"]])
            
            results.append({
                "id": v.id,
                "name": v.name,
                "contact_person": v.contact_person,
                "email": v.email,
                "phone": v.phone,
                "supplied_items": supplied_items,
                "average_delivery_days": v.average_delivery_days,
                "reliability_score": v.reliability_score,
                "total_orders": len(pos),
                "total_value": total_value,
                "active_orders": active_orders
            })
        return results
