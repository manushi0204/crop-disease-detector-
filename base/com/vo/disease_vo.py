from base import db


class DiseaseVO(db.Model):
    __tablename__ = 'diseases'

    disease_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disease_name = db.Column(db.String(100), nullable=False)
    disease_description=db.Column(db.String(500), nullable=False)
    disease_crop_id = db.Column(db.Integer, db.ForeignKey('crops.crop_id'), nullable=False)

    crop = db.relationship('CropVO', backref='diseases')

    def as_dict(self):
        return {
            'disease_id': self.disease_id,
            'disease_name': self.disease_name,
            'disease_description':self.disease_description


        }
db.create_all()

