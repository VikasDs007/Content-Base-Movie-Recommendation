import streamlit as st
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import gc
import time
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="CineMatch - Movie Recommendations",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS that won't cause HTML rendering issues
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #ff6b6b;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class MovieRecommendationSystem:
    """
    A content-based movie recommendation system using TF-IDF and cosine similarity.
    """
    
    def __init__(self, data_path='data/movies.csv', max_features=5000):
        self.data_path = data_path
        self.max_features = max_features
        self.movie_data = None
        self.tfidf_vectorizer = None
        self.feature_vectors = None
        self.similarity_matrix = None
        
    @st.cache_data
    def load_data(_self):
        """Load and cache the movie dataset"""
        try:
            _self.movie_data = pd.read_csv(_self.data_path)
            return _self.movie_data
        except FileNotFoundError:
            st.error(f"❌ Could not find the movie dataset at {_self.data_path}")
            st.info("Please make sure the movies.csv file is in the data/ folder")
            return None
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            return None
    
    def preprocess_features(self, selected_features=['genres', 'description', 'directors', 'stars']):
        """Preprocess and combine movie features with proper weighting"""
        # Handle missing values
        for feature in selected_features:
            if feature in self.movie_data.columns:
                self.movie_data[feature] = self.movie_data[feature].fillna('')
        
        # Clean and process text data
        combined_features = []
        for idx, row in self.movie_data.iterrows():
            feature_text = ""
            
            for feature in selected_features:
                if feature in self.movie_data.columns:
                    text = str(row[feature]).lower()
                    # Remove brackets and quotes from list-like strings
                    text = text.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
                    
                    # Add feature multiple times based on importance
                    weight = self._get_feature_weight(feature)
                    feature_text += (text + " ") * weight
            
            combined_features.append(feature_text.strip())
        
        return combined_features
    
    def _get_feature_weight(self, feature):
        """Get weight for different features based on importance"""
        weights = {
            'genres': 3,      # Most important for content similarity
            'directors': 2,   # Important for style similarity
            'stars': 2,       # Important for cast similarity
            'description': 1  # Provides context but can be noisy
        }
        return weights.get(feature, 1)
    
    @st.cache_data
    def build_similarity_matrix(_self, combined_features):
        """Build TF-IDF vectors and similarity matrix efficiently"""
        # Initialize TF-IDF vectorizer with optimized parameters
        _self.tfidf_vectorizer = TfidfVectorizer(
            max_features=_self.max_features,
            stop_words='english',
            ngram_range=(1, 2),  # Include unigrams and bigrams
            min_df=2,            # Ignore terms in less than 2 documents
            max_df=0.8,          # Ignore terms in more than 80% of documents
            lowercase=True,
            strip_accents='unicode'
        )
        
        # Fit and transform the features
        _self.feature_vectors = _self.tfidf_vectorizer.fit_transform(combined_features)
        
        # For large datasets, we'll compute similarity on-demand
        if _self.feature_vectors.shape[0] > 10000:
            _self.similarity_matrix = None
        else:
            _self.similarity_matrix = cosine_similarity(_self.feature_vectors)
        
        return _self.feature_vectors
    
    def get_movie_recommendations(self, movie_title, num_recommendations=10):
        """Get movie recommendations based on similarity"""
        # Find the movie in the dataset using fuzzy matching
        movie_matches = difflib.get_close_matches(
            movie_title.lower(), 
            [title.lower() for title in self.movie_data['title'].tolist()], 
            n=3, 
            cutoff=0.6
        )
        
        if not movie_matches:
            return {
                'error': f"Movie '{movie_title}' not found in the dataset",
                'suggestions': self._get_movie_suggestions(movie_title)
            }
        
        # Find the exact match in the original data
        matched_movie = None
        movie_index = None
        
        for match in movie_matches:
            for idx, title in enumerate(self.movie_data['title']):
                if title.lower() == match:
                    matched_movie = title
                    movie_index = idx
                    break
            if matched_movie:
                break
        
        if movie_index is None:
            return {'error': 'Movie index not found'}
        
        # Compute similarity scores
        if self.similarity_matrix is not None:
            similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))
        else:
            movie_vector = self.feature_vectors[movie_index:movie_index+1]
            similarity_scores = cosine_similarity(movie_vector, self.feature_vectors).flatten()
            similarity_scores = list(enumerate(similarity_scores))
        
        # Sort by similarity score (excluding the movie itself)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:]
        
        # Get top recommendations
        recommendations = []
        for i in range(min(num_recommendations, len(similarity_scores))):
            movie_idx = similarity_scores[i][0]
            similarity_score = similarity_scores[i][1]
            
            movie_info = {
                'title': self.movie_data.iloc[movie_idx]['title'],
                'similarity_score': round(float(similarity_score), 4)
            }
            
            # Add additional info if available
            for col in ['genres', 'year', 'rating', 'description']:
                if col in self.movie_data.columns:
                    value = self.movie_data.iloc[movie_idx][col]
                    if col == 'description' and len(str(value)) > 150:
                        value = str(value)[:150] + "..."
                    movie_info[col] = value
            
            recommendations.append(movie_info)
        
        return {
            'input_movie': matched_movie,
            'input_movie_info': {
                'genres': self.movie_data.iloc[movie_index]['genres'],
                'year': self.movie_data.iloc[movie_index]['year'],
                'rating': self.movie_data.iloc[movie_index]['rating'],
                'description': self.movie_data.iloc[movie_index]['description']
            },
            'recommendations': recommendations
        }
    
    def _get_movie_suggestions(self, movie_title, n=5):
        """Get movie title suggestions for failed searches"""
        all_titles = self.movie_data['title'].tolist()
        suggestions = difflib.get_close_matches(movie_title, all_titles, n=n, cutoff=0.3)
        return suggestions
    
    def fit(self, selected_features=['genres', 'description', 'directors', 'stars']):
        """Complete pipeline to fit the recommendation system"""
        # Load data
        if self.load_data() is None:
            return None
        
        # Preprocess features
        combined_features = self.preprocess_features(selected_features)
        
        # Build similarity matrix
        self.build_similarity_matrix(combined_features)
        
        return self
    
    def get_random_movies(self, n=10):
        """Get random movies for testing"""
        if self.movie_data is not None:
            sample_movies = self.movie_data.sample(n=n)[['title', 'year', 'genres', 'rating']]
            return sample_movies.to_dict('records')
        return []

# Initialize the recommendation system
@st.cache_resource
def load_recommendation_system():
    """Load and cache the recommendation system"""
    with st.spinner("🔄 Loading movie database and building recommendation system..."):
        recommender = MovieRecommendationSystem()
        if recommender.fit() is None:
            return None
        return recommender

def display_movie_card(movie, rank, show_similarity=True, show_description=True):
    """Display a movie card using only Streamlit native components"""
    
    # Create a container for the movie
    with st.container():
        # Movie title and rank
        st.subheader(f"#{rank} 🎬 {movie['title']} ({movie.get('year', 'N/A')})")
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if show_similarity:
                st.metric("🎯 Similarity", f"{movie['similarity_score']:.4f}")
        
        with col2:
            st.metric("⭐ Rating", movie.get('rating', 'N/A'))
        
        with col3:
            # Count genres
            genres_str = str(movie.get('genres', ''))
            genre_count = len([g.strip() for g in genres_str.replace('[', '').replace(']', '').replace("'", '').replace('"', '').split(',') if g.strip()])
            st.metric("🎭 Genres", genre_count)
        
        # Display genres as tags
        genres_str = str(movie.get('genres', ''))
        genres_clean = genres_str.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
        genre_list = [g.strip() for g in genres_clean.split(',') if g.strip()][:4]
        
        if genre_list:
            st.write("**Genres:** " + " • ".join(genre_list))
        
        # Description
        if show_description and movie.get('description'):
            with st.expander("📖 Description"):
                st.write(movie['description'])
        
        st.divider()

def main():
    # Header using only Streamlit components
    st.markdown('<div class="main-title">🎭 CineMatch</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Discover your next favorite movie with AI-powered recommendations</div>', unsafe_allow_html=True)
    
    # Load system
    recommender = load_recommendation_system()
    
    if recommender is None:
        st.error("❌ Failed to load the recommendation system. Please check your data file.")
        st.info("**Troubleshooting:**")
        st.write("• Ensure movies.csv is in the data/ folder")
        st.write("• Check file permissions")
        st.write("• Verify CSV format and columns")
        return
    
    st.success(f"✅ CineMatch AI is ready! Database loaded with {len(recommender.movie_data):,} movies.")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Settings")
        num_recommendations = st.slider("Number of recommendations", 1, 20, 5)
        
        with st.expander("🔧 Advanced Settings"):
            show_descriptions = st.checkbox("Show movie descriptions", value=True)
            show_similarity_scores = st.checkbox("Show similarity scores", value=True)
            sort_by_rating = st.checkbox("Sort by rating", value=False)
        
        st.divider()
        
        # Quick search in sidebar
        st.subheader("⚡ Quick Search")
        quick_search = st.text_input(
            "",
            placeholder="🔍 Quick movie search...",
            key="quick_search",
            label_visibility="collapsed"
        )
        
        if quick_search:
            # Show quick search results
            matching_movies = recommender.movie_data[
                recommender.movie_data['title'].str.contains(quick_search, case=False, na=False)
            ].head(5)
            
            if not matching_movies.empty:
                st.write("**🎬 Found:**")
                for _, movie in matching_movies.iterrows():
                    if st.button(
                        f"{movie['title']} ({movie['year']})", 
                        key=f"quick_{movie['title']}", 
                        use_container_width=True
                    ):
                        st.session_state.selected_movie = movie['title']
                        st.rerun()
        
        st.divider()
        
        # Dataset stats using native components
        st.subheader("📊 Database Stats")
        st.metric("🎬 Total Movies", f"{len(recommender.movie_data):,}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📅 Year Range", f"{recommender.movie_data['year'].min():.0f}-{recommender.movie_data['year'].max():.0f}")
        with col2:
            st.metric("⭐ Rating Range", f"{recommender.movie_data['rating'].min():.1f}-{recommender.movie_data['rating'].max():.1f}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Find Your Next Movie")
        
        movie_title = st.text_input(
            "Enter a movie title:",
            placeholder="e.g., The Dark Knight, Inception, Titanic...",
            help="Type the name of a movie you like to get AI-powered recommendations"
        )
        
        # Search button
        search_clicked = st.button("🎭 Get Recommendations", type="primary", use_container_width=True)
        
        # Example movies
        with st.expander("💡 Need inspiration? Try these popular movies"):
            example_movies = ["The Dark Knight", "Inception", "Pulp Fiction", "The Godfather", "Forrest Gump", "The Matrix"]
            
            # Create columns for example buttons
            cols = st.columns(3)
            for i, movie in enumerate(example_movies):
                with cols[i % 3]:
                    if st.button(movie, key=f"example_{movie}", use_container_width=True):
                        movie_title = movie
                        st.rerun()
        
        if search_clicked and movie_title:
            with st.spinner("🔍 Finding similar movies..."):
                recommendations = recommender.get_movie_recommendations(movie_title, num_recommendations)
            
            if 'error' in recommendations:
                st.error(f"❌ {recommendations['error']}")
                
                if 'suggestions' in recommendations and recommendations['suggestions']:
                    st.info("💡 Did you mean one of these?")
                    suggestion_cols = st.columns(min(3, len(recommendations['suggestions'])))
                    for i, suggestion in enumerate(recommendations['suggestions']):
                        with suggestion_cols[i % 3]:
                            if st.button(f"🎬 {suggestion}", key=f"suggestion_{suggestion}", use_container_width=True):
                                st.rerun()
            else:
                # Display input movie info
                input_info = recommendations['input_movie_info']
                
                st.success(f"✅ Found: **{recommendations['input_movie']}**")
                
                # Input movie metrics
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("📅 Year", input_info.get('year', 'N/A'))
                with col_b:
                    st.metric("⭐ Rating", input_info.get('rating', 'N/A'))
                with col_c:
                    genres_count = len(str(input_info.get('genres', '')).split(','))
                    st.metric("🎭 Genres", genres_count)
                
                if input_info.get('description') and show_descriptions:
                    with st.expander("📖 Movie Description"):
                        st.write(input_info['description'])
                
                st.divider()
                
                # Display recommendations
                st.header(f"🎯 Your Top {len(recommendations['recommendations'])} Recommendations")
                
                recs = recommendations['recommendations']
                if sort_by_rating:
                    recs = sorted(recs, key=lambda x: float(x.get('rating', 0)), reverse=True)
                
                # Display each recommendation using the native card function
                for i, movie in enumerate(recs, 1):
                    display_movie_card(movie, i, show_similarity_scores, show_descriptions)
        
        elif search_clicked:
            st.warning("⚠️ Please enter a movie title to get started")
    
    with col2:
        st.header("🎲 Discover Movies")
        st.write("Need inspiration? Explore random movies from our database:")
        
        if st.button("🔄 Get Random Movies", use_container_width=True):
            random_movies = recommender.get_random_movies(5)
            
            for movie in random_movies:
                with st.container():
                    st.subheader(f"🎬 {movie['title']}")
                    
                    col_year, col_rating = st.columns(2)
                    with col_year:
                        st.write(f"📅 **Year:** {movie['year']}")
                    with col_rating:
                        st.write(f"⭐ **Rating:** {movie['rating']}")
                    
                    # Clean and display genres
                    genres_str = str(movie.get('genres', ''))
                    genres_clean = genres_str.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
                    genre_list = [g.strip() for g in genres_clean.split(',') if g.strip()][:3]
                    if genre_list:
                        st.write(f"🎭 **Genres:** {', '.join(genre_list)}")
                    
                    st.divider()
        
        st.divider()
        
        # Popular genres analysis
        st.subheader("🔥 Popular Genres")
        
        # Analyze genres
        all_genres = []
        for genres in recommender.movie_data['genres'].dropna():
            if isinstance(genres, str):
                clean_genres = genres.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
                genre_list = [g.strip() for g in clean_genres.split(',') if g.strip()]
                all_genres.extend(genre_list)
        
        if all_genres:
            genre_counts = pd.Series(all_genres).value_counts().head(5)
            
            for genre, count in genre_counts.items():
                st.write(f"🎭 **{genre}:** {count:,} movies")

def add_footer():
    """Add a stylish footer"""
    st.markdown("---")
    st.markdown('''
    <div style="text-align: center; padding: 2rem; color: #a0a0a0;">
        <div style="margin-bottom: 1rem;">
            <span style="font-size: 1.5rem;">🎭</span>
            <span style="color: #ff6b6b; font-weight: 600; margin: 0 1rem;">CineMatch</span>
            <span style="font-size: 1.5rem;">🎬</span>
        </div>
        <div style="font-size: 0.9rem;">
            Powered by AI • Built with ❤️ using Streamlit
        </div>
        <div style="margin-top: 0.5rem; font-size: 0.8rem;">
            Discover • Watch • Enjoy
        </div>
    </div>
    ''', unsafe_allow_html=True)

def add_loading_animation():
    """Add a custom loading animation"""
    return st.markdown('''
    <div class="loading-container">
        <div class="loading-spinner"></div>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    add_footer()