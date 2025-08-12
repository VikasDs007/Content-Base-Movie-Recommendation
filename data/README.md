# Dataset Directory

This directory contains the movie dataset used by CineMatch.

## Included Dataset

The `movies.csv` file contains a comprehensive movie database with 60K+ movies from IMDb.

## Dataset Format

Your CSV file should include the following columns:

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| `title` | string | ✅ | Movie title | "The Dark Knight" |
| `year` | integer | ✅ | Release year | 2008 |
| `genres` | string/list | ✅ | Movie genres | "Action, Crime, Drama" or ["Action", "Crime", "Drama"] |
| `description` | string | ✅ | Plot summary | "When the menace known as the Joker..." |
| `directors` | string/list | ✅ | Director names | "Christopher Nolan" or ["Christopher Nolan"] |
| `stars` | string/list | ✅ | Main actors | "Christian Bale, Heath Ledger" or ["Christian Bale", "Heath Ledger"] |
| `rating` | float | ✅ | IMDb rating | 9.0 |
| `votes` | string | ❌ | Number of votes | "2.5M" |
| `duration` | string | ❌ | Movie length | "2h 32m" |
| `MPA` | string | ❌ | Rating (PG, R, etc.) | "PG-13" |

## Sample Data

Here's an example of how your data should look:

```csv
title,year,genres,description,directors,stars,rating
"The Dark Knight",2008,"Action, Crime, Drama","When the menace known as the Joker wreaks havoc...","Christopher Nolan","Christian Bale, Heath Ledger, Aaron Eckhart",9.0
"Inception",2010,"Action, Sci-Fi, Thriller","A thief who steals corporate secrets...","Christopher Nolan","Leonardo DiCaprio, Marion Cotillard, Ellen Page",8.8
```

## Data Sources

You can obtain movie datasets from:

### Free Sources
- **IMDb Datasets**: https://www.imdb.com/interfaces/
- **The Movie Database (TMDb)**: https://www.themoviedb.org/documentation/api
- **Kaggle**: Various movie datasets available
- **MovieLens**: https://grouplens.org/datasets/movielens/

### Commercial Sources
- **IMDb Pro**: Professional movie database
- **Rotten Tomatoes API**: Movie ratings and reviews
- **Box Office Mojo**: Box office data

## Data Preprocessing

The application will automatically:
- Handle missing values by filling with empty strings
- Clean text data (remove brackets, quotes)
- Process list-like strings for genres, directors, and stars
- Apply feature weighting for better recommendations

## Dataset Information

📊 **Current Dataset**: 
- **Source**: IMDb public dataset
- **Size**: 60K+ movies
- **License**: Public domain / Fair use for educational/research purposes
- **Content**: Movie titles, genres, descriptions, cast, directors, ratings

## File Size Recommendations

- **Small**: < 1MB (1K-5K movies) - Great for testing
- **Medium**: 1-50MB (5K-50K movies) - Good performance
- **Large**: 50-200MB (50K-100K movies) - May need optimization
- **Very Large**: > 200MB (100K+ movies) - Consider data sampling

## Troubleshooting

### Common Issues

1. **File not found error**
   - Ensure `movies.csv` is in the `data/` directory
   - Check file name spelling and case sensitivity

2. **Column missing error**
   - Verify all required columns are present
   - Check column name spelling

3. **Encoding issues**
   - Save CSV with UTF-8 encoding
   - Handle special characters properly

4. **Performance issues**
   - Consider reducing dataset size for testing
   - Use data sampling for very large datasets

### Data Quality Tips

- **Remove duplicates**: Ensure unique movie entries
- **Standardize formats**: Consistent date and rating formats
- **Clean text**: Remove HTML tags, special characters
- **Validate data**: Check for reasonable values (years, ratings)

## Example Datasets

For testing purposes, you can create a small sample dataset:

```python
import pandas as pd

sample_data = {
    'title': ['The Dark Knight', 'Inception', 'Pulp Fiction'],
    'year': [2008, 2010, 1994],
    'genres': ['Action, Crime, Drama', 'Action, Sci-Fi, Thriller', 'Crime, Drama'],
    'description': [
        'When the menace known as the Joker wreaks havoc...',
        'A thief who steals corporate secrets...',
        'The lives of two mob hitmen, a boxer...'
    ],
    'directors': ['Christopher Nolan', 'Christopher Nolan', 'Quentin Tarantino'],
    'stars': ['Christian Bale, Heath Ledger', 'Leonardo DiCaprio', 'John Travolta, Samuel L. Jackson'],
    'rating': [9.0, 8.8, 8.9]
}

df = pd.DataFrame(sample_data)
df.to_csv('data/movies.csv', index=False)
```

---

**Need help?** Check our [Contributing Guide](../CONTRIBUTING.md) or open an issue on GitHub.