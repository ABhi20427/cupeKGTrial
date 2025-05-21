# services/nlp_service.py
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class NLPService:
    def __init__(self):
        # Initialize the models
        self.qa_model = None
        self.sentiment_model = None
    
    def _load_qa_model(self):
        """Lazy load the question answering model"""
        if self.qa_model is None:
            try:
                model_name = "deepset/roberta-base-squad2"
                self.qa_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
                self.qa_pipeline = pipeline("question-answering", model=self.qa_model, tokenizer=self.qa_tokenizer)
                logger.info("QA model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading QA model: {e}")
                raise
    
    def _load_sentiment_model(self):
        """Lazy load the sentiment analysis model"""
        if self.sentiment_model is None:
            try:
                self.sentiment_model = pipeline("sentiment-analysis")
                logger.info("Sentiment model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading sentiment model: {e}")
                raise
    
    def answer_question(self, question: str, context: str) -> Dict[str, Any]:
        """
        Answer a question based on the provided context
        """
        self._load_qa_model()
        
        try:
            result = self.qa_pipeline({
                'question': question,
                'context': context
            })
            
            return {
                'answer': result['answer'],
                'confidence': result['score'],
                'start': result['start'],
                'end': result['end']
            }
        except Exception as e:
            logger.error(f"Error in question answering: {e}")
            return {
                'answer': "I couldn't find an answer to that question.",
                'confidence': 0.0,
                'error': str(e)
            }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of the given text
        """
        self._load_sentiment_model()
        
        try:
            result = self.sentiment_model(text)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                'label': 'unknown',
                'score': 0.0,
                'error': str(e)
            }
    
    def get_location_recommendations(self, user_interests: List[str], 
                                   visited_locations: List[str]) -> List[Dict[str, Any]]:
        """
        Get personalized location recommendations based on user interests
        """
        # This would be implemented with more advanced NLP/ML techniques
        # For now, return a simple placeholder
        return [
            {
                'id': 'konark',
                'name': 'Konark',
                'reason': 'Based on your interest in architecture and temples'
            },
            {
                'id': 'delhi',
                'name': 'Delhi',
                'reason': 'Recommended for cultural diversity'
            }
        ]