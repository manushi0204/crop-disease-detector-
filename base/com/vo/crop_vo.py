from base import db


class CropVO(db.Model):
    __tablename__ = 'crops'

    crop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crop_name = db.Column(db.String(100), nullable=False)


    crop_description = db.Column(db.Text)


    def as_dict(self):
        return {
            'crop_id': self.crop_id,
            'crop_name': self.crop_name,
            'crop_description': self.crop_description,

        }
