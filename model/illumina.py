from __init__ import db

class GeneRecord(db.Model):
    __tablename__ = 'genes'  
    
    id = db.Column(db.Integer, primary_key=True)
    gene = db.Column(db.String(64), nullable=False)
    condition = db.Column(db.String(255), nullable=False)
    mutation = db.Column(db.String(32), nullable=False)
    sequence = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)

    def __init__(self, gene, condition, mutation, sequence, correct):
        self.gene = gene
        self.condition = condition
        self.mutation = mutation
        self.sequence = sequence
        self.correct = correct

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"[DB ERROR] Could not save GeneRecord: {e}")
            return None

    def read(self):
        return {
            "id": self.id,
            "gene": self.gene,
            "condition": self.condition,
            "mutation": self.mutation,
            "sequence": self.sequence,
            "correct": self.correct
        }

# ✅ Optional function to create the table if needed
def initGeneRecord():
    from __init__ import app
    with app.app_context():
        db.create_all()
        print(" genes table created.")
