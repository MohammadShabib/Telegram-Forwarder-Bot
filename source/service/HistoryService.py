import logging
from typing import Optional, Dict, Tuple

from source.model.History import History

logger = logging.getLogger(__name__)

class HistoryService:
    """Service for managing message history and mappings between source and destination messages."""
    
    def __init__(self):
        """Initialize the history service with the history model."""
        self._history = History()

    def add_mapping(self, source_chat_id: int, source_msg_id: int, dest_chat_id: int, dest_msg_id: int) -> None:
        """Add a mapping between source and destination messages.
        
        Args:
            source_chat_id: ID of the source chat
            source_msg_id: ID of the source message
            dest_chat_id: ID of the destination chat
            dest_msg_id: ID of the destination message
        """
        try:
            self._history.add_mapping(source_chat_id, source_msg_id, dest_chat_id, dest_msg_id)
        except Exception as e:
            logger.error(f"Error adding message mapping: {e}", exc_info=True)

    def get_mapping(self, source_chat_id: int, source_msg_id: int, dest_chat_id: int) -> Optional[int]:
        """Get the destination message ID for a source message.
        
        Args:
            source_chat_id: ID of the source chat
            source_msg_id: ID of the source message
            dest_chat_id: ID of the destination chat
            
        Returns:
            Destination message ID if found, None otherwise
        """
        try:
            return self._history.get_mapping(source_chat_id, source_msg_id, dest_chat_id)
        except Exception as e:
            logger.error(f"Error getting message mapping: {e}", exc_info=True)
            return None

    def get_all_mappings(self) -> Dict[Tuple[int, int, int], int]:
        """Get all message mappings.
        
        Returns:
            Dictionary of all message mappings
        """
        return self._history.message_map 