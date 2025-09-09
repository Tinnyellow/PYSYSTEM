"""
Contact value object with email and phone validation.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Contact:
    """Contact value object with validation."""
    
    email: str
    phone: str
    
    def __post_init__(self):
        """Validate contact after initialization."""
        # Clean phone number
        clean_phone = re.sub(r'\D', '', self.phone)
        object.__setattr__(self, 'phone', clean_phone)
        
        self._validate_contact()
    
    def _validate_contact(self) -> None:
        """Validate contact data."""
        if not self._is_valid_email():
            raise ValueError("Invalid email format")
        
        if not self._is_valid_phone():
            raise ValueError("Invalid phone format. Must include area code and number")
    
    def _is_valid_email(self) -> bool:
        """Validate email format."""
        if not self.email or not self.email.strip():
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, self.email.strip()))
    
    def _is_valid_phone(self) -> bool:
        """Validate phone format (Brazilian format with area code)."""
        if not self.phone:
            return False
        
        # Brazilian phone: area code (2 digits) + number (8 or 9 digits)
        # Total: 10 digits (landline) or 11 digits (mobile)
        return len(self.phone) in [10, 11] and self.phone.isdigit()
    
    def get_formatted_phone(self) -> str:
        """Get formatted phone number."""
        if len(self.phone) == 10:
            # Landline: (11) 1234-5678
            return f"({self.phone[:2]}) {self.phone[2:6]}-{self.phone[6:]}"
        elif len(self.phone) == 11:
            # Mobile: (11) 91234-5678
            return f"({self.phone[:2]}) {self.phone[2:7]}-{self.phone[7:]}"
        return self.phone
    
    def get_display_info(self) -> str:
        """Get formatted contact information."""
        return f"Email: {self.email} | Phone: {self.get_formatted_phone()}"
    
    def __str__(self) -> str:
        """String representation."""
        return self.get_display_info()
