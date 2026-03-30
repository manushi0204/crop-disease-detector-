from base import app, db
from base.com.vo.crop_vo import CropVO
from base.com.vo.disease_vo import DiseaseVO

with app.app_context():
    db.session.query(DiseaseVO).delete()
    db.session.query(CropVO).delete()
    db.session.commit()
    print("All test data cleaned!")
