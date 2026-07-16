import type { NewsSourceType } from './types';
import { ArticleCard } from './ArticleCard';
import { BrowserRouter, Routes, Route, Link, Outlet } from 'react-router-dom';

export const ChannelColumn: React.FC<{ source: NewsSourceType }> = ({ source }) => {
  const displayed = source.Articles
  const displayedArticles = displayed.length > 3 ? displayed.slice(0, 3) : displayed;

  return (
    <div style={{
      flex: '1', minWidth: '300px', backgroundColor: '#F9FAFB', 
      padding: '20px', borderRadius: '10px', border: '1px solid #E5E7EB'
    }}>
      <div style={{ borderBottom: '3px solid #DC2626', paddingBottom: '10px', marginBottom: '20px' }}>
        <h2 style={{ margin: '0', color: '#1E3A8A', fontSize: '1.5rem', textTransform: 'uppercase' }}>
          {source.name}
        </h2>
        <span style={{ fontSize: '0.8rem', color: '#6B7280', textTransform: 'uppercase', letterSpacing: '1px' }}>
          {source.category}
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {displayedArticles.length > 0 ? (
          displayedArticles.map(Article => (
            <ArticleCard key={Article.id} article={Article} />
          ))
        ) : (
          <p style={{ color: '#9CA3AF', fontStyle: 'italic' }}>Nu există stiri recente.</p>
        )}
      </div>

      {source.Articles.length > 3 && (
        <Link to={`/canal/${source.id}-${source.name}`}
        style={{
            display: 'block', 
            textAlign: 'center',
            textDecoration: 'none', 
            width: '100%', 
            padding: '12px', 
            marginTop: '10px',
            backgroundColor: '#1E3A8A',
            color: 'white',
            border: 'none', 
            borderRadius: '6px', 
            fontWeight: 'bold',
            boxSizing: 'border-box'
          }}
        >
          Vezi toate cele {source.Articles.length} știri
        </Link>
         
      )}
    </div>
  );
};