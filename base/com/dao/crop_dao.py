from base import db
from base.com.vo.crop_vo import CropVO


class CropDAO:

    def insert_crop(self, crop_vo):
        try:
            db.session.add(crop_vo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("ERROR in insert_crop:", e)

    def view_all_crops(self):
        try:
            return CropVO.query.all()
        except Exception as e:
            print("ERROR in view_all_crops:", e)

    def get_by_id(self, crop_id):
        try:
            return CropVO.query.get(crop_id)
        except Exception as e:
            print("ERROR in get_by_id:", e)

    def update_crop(self, crop_vo):
        try:
            existing = CropVO.query.filter_by(crop_id=crop_vo.crop_id).first()
            existing.crop_name = crop_vo.crop_name
            existing.crop_description = crop_vo.crop_description
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("ERROR in update_crop:", e)

    def delete_crop(self, crop_vo):
        try:
            crop = CropVO.query.get(crop_vo.crop_id)
            db.session.delete(crop)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("ERROR in delete_crop:", e)