# cupe-kg-backend/services/nlp_service.py

"""
Advanced NLP Service for CuPe-KG
Implements BERT-based cultural context extraction and analysis
"""

import logging
import re
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optional imports - will fallback to basic implementation if not available
try:
    from transformers import AutoTokenizer, AutoModel, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers not available, using basic NLP implementation")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logging.warning("TextBlob not available, sentiment analysis disabled")

logger = logging.getLogger(__name__)

class NLPService:
    """Advanced NLP service for cultural tourism context extraction"""
    
    def __init__(self):
        self.models_loaded = False
        self.cultural_keywords = self._initialize_cultural_keywords()
        self.dynasty_patterns = self._initialize_dynasty_patterns()
        self.architectural_styles = self._initialize_architectural_styles()
        
        # Initialize vectorizer for similarity calculations
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 3)
        )
        
        self._load_models()
    
    def _load_models(self):
        """Load BERT and other NLP models"""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Using basic NLP implementation without BERT")
            return
        
        try:
            # Load BERT model for embeddings
            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            self.bert_model = AutoModel.from_pretrained('bert-base-uncased')
            
            # Load sentiment analysis pipeline
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            
            # Load NER pipeline for entity extraction
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple"
            )
            
            self.models_loaded = True
            logger.info("NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading NLP models: {e}")
            self.models_loaded = False
    
    def _initialize_cultural_keywords(self) -> Dict[str, List[str]]:
        """Initialize cultural theme keywords for classification"""
        return {
            'architectural': [
                'temple', 'mosque', 'fort', 'palace', 'monument', 'architecture',
                'dome', 'minaret', 'pillar', 'carving', 'sculpture', 'facade',
                'gopuram', 'shikhara', 'mandapa', 'vimana'
            ],
            'religious': [
                'spiritual', 'sacred', 'holy', 'divine', 'worship', 'prayer',
                'pilgrimage', 'devotion', 'ritual', 'ceremony', 'festival',
                'meditation', 'enlightenment', 'blessing'
            ],
            'historical': [
                'ancient', 'medieval', 'colonial', 'empire', 'dynasty', 'ruler',
                'battle', 'conquest', 'kingdom', 'capital', 'heritage', 'legacy',
                'chronicle', 'inscription', 'manuscript'
            ],
            'cultural': [
                'tradition', 'custom', 'folklore', 'legend', 'myth', 'story',
                'dance', 'music', 'art', 'craft', 'literature', 'philosophy',
                'language', 'dialect', 'community', 'society'
            ],
            'artistic': [
                'painting', 'fresco', 'mural', 'sculpture', 'carving', 'relief',
                'decoration', 'ornament', 'pattern', 'motif', 'style', 'technique',
                'craftsmanship', 'artistry', 'aesthetic'
            ]
        }
    
    def _initialize_dynasty_patterns(self) -> Dict[str, List[str]]:
        """Initialize dynasty and empire recognition patterns"""
        return {
            'Mughal': ['mughal', 'mogul', 'shah jahan', 'akbar', 'aurangzeb', 'babur', 'humayun'],
            'Vijayanagara': ['vijayanagara', 'hampi', 'krishnadevaraya', 'harihara', 'bukka'],
            'Chola': ['chola', 'cholan', 'rajaraja', 'rajendra', 'thanjavur'],
            'Mauryan': ['maurya', 'mauryan', 'ashoka', 'chandragupta', 'pataliputra'],
            'Gupta': ['gupta', 'chandragupta', 'samudragupta', 'golden age'],
            'Delhi Sultanate': ['delhi sultanate', 'slave dynasty', 'khilji', 'tughlaq', 'lodi'],
            'Maratha': ['maratha', 'shivaji', 'peshwa', 'pune', 'satara'],
            'Rajput': ['rajput', 'rajputana', 'mewar', 'marwar', 'amber'],
            'British': ['british', 'colonial', 'east india company', 'raj', 'victorian']
        }
    
    def _initialize_architectural_styles(self) -> Dict[str, List[str]]:
        """Initialize architectural style recognition patterns"""
        return {
            'Dravidian': ['dravidian', 'south indian', 'gopuram', 'vimana', 'tamil'],
            'Nagara': ['nagara', 'north indian', 'shikhara', 'kalasha'],
            'Indo-Islamic': ['indo-islamic', 'indo-saracenic', 'minaret', 'dome', 'arch'],
            'Colonial': ['colonial', 'british', 'victorian', 'neoclassical', 'gothic'],
            'Vesara': ['vesara', 'hybrid', 'hoysala', 'chalukya'],
            'Buddhist': ['buddhist', 'stupa', 'chaitya', 'vihara', 'monastery'],
            'Jain': ['jain', 'jaina', 'tirthankara', 'dilwara']
        }
    
    def extract_cultural_entities(self, text: str) -> Dict[str, Any]:
        """Extract cultural entities and themes from text"""
        entities = {
            'cultural_themes': [],
            'dynasties': [],
            'architectural_styles': [],
            'named_entities': [],
            'time_periods': [],
            'locations': []
        }
        
        text_lower = text.lower()
        
        # Extract cultural themes
        for theme, keywords in self.cultural_keywords.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                entities['cultural_themes'].append({
                    'theme': theme,
                    'keywords': matches,
                    'confidence': len(matches) / len(keywords)
                })
        
        # Extract dynasties
        for dynasty, patterns in self.dynasty_patterns.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                entities['dynasties'].append({
                    'dynasty': dynasty,
                    'patterns': matches,
                    'confidence': len(matches) / len(patterns)
                })
        
        # Extract architectural styles
        for style, patterns in self.architectural_styles.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                entities['architectural_styles'].append({
                    'style': style,
                    'patterns': matches,
                    'confidence': len(matches) / len(patterns)
                })
        
        # Extract time periods using regex
        time_patterns = [
            r'(\d{1,4})\s*(?:CE|AD|BC|BCE)',
            r'(\d{1,2})(?:st|nd|rd|th)\s*century',
            r'(\d{1,4})\s*-\s*(\d{1,4})\s*(?:CE|AD|BC|BCE)'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['time_periods'].extend(matches)
        
        # Use BERT-based NER if available
        if self.models_loaded and TRANSFORMERS_AVAILABLE:
            try:
                ner_results = self.ner_pipeline(text)
                entities['named_entities'] = [
                    {
                        'text': ent['word'],
                        'label': ent['entity_group'],
                        'confidence': ent['score']
                    }
                    for ent in ner_results
                    if ent['score'] > 0.7
                ]
            except Exception as e:
                logger.error(f"Error in NER extraction: {e}")
        
        return entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of cultural text"""
        if self.models_loaded and TRANSFORMERS_AVAILABLE:
            try:
                results = self.sentiment_analyzer(text)
                return {
                    'sentiment': results[0]['label'].lower(),
                    'confidence': results[0]['score'],
                    'all_scores': {r['label'].lower(): r['score'] for r in results}
                }
            except Exception as e:
                logger.error(f"Error in sentiment analysis: {e}")
        
        # Fallback to TextBlob if available
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                
                if polarity > 0.1:
                    sentiment = 'positive'
                elif polarity < -0.1:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                
                return {
                    'sentiment': sentiment,
                    'confidence': abs(polarity),
                    'polarity': polarity,
                    'subjectivity': blob.sentiment.subjectivity
                }
            except Exception as e:
                logger.error(f"Error in TextBlob sentiment analysis: {e}")
        
        # Basic keyword-based sentiment
        positive_words = ['beautiful', 'magnificent', 'stunning', 'amazing', 'wonderful', 'impressive']
        negative_words = ['destroyed', 'ruined', 'damaged', 'neglected', 'deteriorated']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            confidence = pos_count / (pos_count + neg_count + 1)
        elif neg_count > pos_count:
            sentiment = 'negative'
            confidence = neg_count / (pos_count + neg_count + 1)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'positive_indicators': pos_count,
            'negative_indicators': neg_count
        }
    
    def get_bert_embeddings(self, text: str) -> np.ndarray:
        """Get BERT embeddings for semantic similarity"""
        if not self.models_loaded:
            return np.array([])
        
        try:
            # Tokenize and encode
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding=True,
                max_length=512
            )
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
            
            return embeddings.numpy()
            
        except Exception as e:
            logger.error(f"Error generating BERT embeddings: {e}")
            return np.array([])
    
    def calculate_cultural_similarity(self, text1: str, text2: str) -> float:
        """Calculate cultural context similarity between two texts"""
        if self.models_loaded:
            # Use BERT embeddings for similarity
            emb1 = self.get_bert_embeddings(text1)
            emb2 = self.get_bert_embeddings(text2)
            
            if emb1.size > 0 and emb2.size > 0:
                # Cosine similarity
                similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
                return float(similarity)
        
        # Fallback to TF-IDF similarity
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def classify_cultural_type(self, text: str) -> Dict[str, Any]:
        """Classify the cultural type of a location or text"""
        entities = self.extract_cultural_entities(text)
        
        # Calculate scores for each cultural category
        scores = {}
        for theme_data in entities['cultural_themes']:
            theme = theme_data['theme']
            confidence = theme_data['confidence']
            scores[theme] = scores.get(theme, 0) + confidence
        
        # Normalize scores
        if scores:
            max_score = max(scores.values())
            if max_score > 0:
                scores = {k: v/max_score for k, v in scores.items()}
        
        # Determine primary classification
        if scores:
            primary_type = max(scores.keys(), key=scores.get)
            primary_confidence = scores[primary_type]
        else:
            primary_type = 'general'
            primary_confidence = 0.5
        
        return {
            'primary_type': primary_type,
            'confidence': primary_confidence,
            'all_scores': scores,
            'extracted_entities': entities
        }
    
    def generate_cultural_summary(self, location_data: Dict[str, Any]) -> str:
        """Generate an AI-powered cultural summary for a location"""
        # Combine all text fields
        text_fields = [
            location_data.get('description', ''),
            location_data.get('history', ''),
            ' '.join(location_data.get('cultural_facts', [])),
            ' '.join([legend.get('description', '') for legend in location_data.get('legends', [])])
        ]
        
        combined_text = ' '.join(text_fields)
        
        # Extract entities and analyze
        entities = self.extract_cultural_entities(combined_text)
        sentiment = self.analyze_sentiment(combined_text)
        classification = self.classify_cultural_type(combined_text)
        
        # Generate summary based on analysis
        summary_parts = []
        
        # Add primary classification
        summary_parts.append(f"This {classification['primary_type']} heritage site")
        
        # Add dynasty information
        if entities['dynasties']:
            dynasty = entities['dynasties'][0]['dynasty']
            summary_parts.append(f"from the {dynasty} period")
        
        # Add architectural style
        if entities['architectural_styles']:
            style = entities['architectural_styles'][0]['style']
            summary_parts.append(f"showcases {style} architecture")
        
        # Add cultural significance
        cultural_themes = [t['theme'] for t in entities['cultural_themes']]
        if 'religious' in cultural_themes:
            summary_parts.append("and holds deep spiritual significance")
        elif 'artistic' in cultural_themes:
            summary_parts.append("and represents exceptional artistic achievement")
        elif 'historical' in cultural_themes:
            summary_parts.append("and marks an important historical milestone")
        
        # Add sentiment context
        if sentiment['sentiment'] == 'positive':
            summary_parts.append("celebrated for its magnificence and cultural importance")
        
        summary = ' '.join(summary_parts) + '.'
        
        return {
            'summary': summary,
            'entities': entities,
            'sentiment': sentiment,
            'classification': classification
        }