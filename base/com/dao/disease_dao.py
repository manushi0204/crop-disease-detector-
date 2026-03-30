from base import db
from base.com.vo.disease_vo import DiseaseVO
from base.com.vo.crop_vo import CropVO


class DiseaseDAO():

    def insert_disease(self, disease_vo):
        try:
            db.session.add(disease_vo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("ERROR in insert_disease:", e)

    def view_disease(self):
        try:
            return db.session.query(DiseaseVO, CropVO).join(
                CropVO, DiseaseVO.disease_crop_id == CropVO.crop_id
            ).all()
        except Exception as e:
            print("ERROR in view_disease:", e)

    def delete_disease(self, disease_id):
        try:
            disease = DiseaseVO.query.get(int(disease_id))
            db.session.delete(disease)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print("ERROR in delete_disease:", e)


    def edit_disease(self, disease_id):
        try:
            return DiseaseVO.query.get(disease_id)
        except Exception as e:
            print("ERROR in edit_disease", e)

    def update_disease(self, disease_vo):
        db.session.merge(disease_vo)
        db.session.commit()