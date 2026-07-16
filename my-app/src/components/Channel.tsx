import { ArticleCard } from './ArticleCard';
import type { NewsSourceType } from './types';

export const Channel: React.FC<{ source: NewsSourceType }> = ({ source }) =>{
  return (
    <div style={{ 
      backgroundColor: '#F9FAFB', 
      padding: '30px', 
      borderRadius: '10px', 
      border: '1px solid #E5E7EB' 
    }}>
      
      <div style={{ borderBottom: '3px solid #DC2626', paddingBottom: '15px', marginBottom: '30px' }}>
        <h1 style={{ margin: '0', color: '#1E3A8A', fontSize: '2.5rem', textTransform: 'uppercase' }}>
          {source.name}
        </h1>
        <span style={{ fontSize: '1rem', color: '#6B7280', textTransform: 'uppercase', letterSpacing: '2px' }}>
          {source.category}
        </span>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '20px' 
      }}>
        {source.Articles && source.Articles.length > 0 ? (
          source.Articles.map(Article => (
            <ArticleCard key={Article.id} article={Article} />
          ))
        ) : (
          <p style={{ color: '#9CA3AF', fontStyle: 'italic', gridColumn: '1 / -1' }}>
            Nu există știri recente pentru acest canal.
          </p>
        )}
      </div>

    </div>
  );
};