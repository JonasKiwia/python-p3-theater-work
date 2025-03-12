from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    
    # Establish a one-to-many relationship with Audition
    auditions = relationship('Audition', back_populates='role')
    
    def actors(self):
        """Return a list of actor names from associated auditions."""
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        """Return a list of locations from associated auditions."""
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        """
        Return the first audition (instance) that was hired for this role.
        If none have been hired, return an appropriate string.
        """
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0]
        else:
            return 'no actor has been hired for this role'
    
    def understudy(self):
        """
        Return the second audition (instance) that was hired for this role.
        If less than two have been hired, return an appropriate string.
        """
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        else:
            return 'no actor has been hired for understudy for this role'

class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    
    # Establish the inverse side of the relationship
    role = relationship('Role', back_populates='auditions')
    
    def call_back(self):
        """Mark the audition as hired by setting hired to True."""
        self.hired = True
        return self
