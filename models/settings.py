from database.db import db

class SiteSettings(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='SignBridge')
    hero_title = db.Column(db.String(255), default='Bridge the Communication Gap Across All Sign Languages')
    hero_subtitle = db.Column(db.Text, default='Real-time sign language translation, multi-language sign library, and interactive learning tools.')
    allow_registration = db.Column(db.Boolean, default=True)
    maintenance_mode = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_settings():
        s = SiteSettings.query.first()
        if not s:
            s = SiteSettings()
            db.session.add(s)
            db.session.commit()
        return s
