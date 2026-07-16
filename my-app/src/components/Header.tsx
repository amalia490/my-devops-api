import { useMutation } from "@apollo/client/react";
import { useState } from "react";
import { SUBSCRIBE_MUTATION } from "./types";

export function Header(){
    const [email, setEmail] = useState('')
    const [subscribe, { loading: mutationLoading }] = useMutation(SUBSCRIBE_MUTATION);

    const handleSubscribe = async (e: React.SubmitEvent) => {
    e.preventDefault();
    
    try {
      const response = await subscribe({
        variables: { email: email, isActive: true }
      });
      alert((response.data as any).addSubscriber);
      setEmail(''); 
        }catch (err: any) {
      console.error(err);
      alert("A apărut o eroare. Te rugăm să încerci din nou!");
        }
    };
    return(
         <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px', paddingBottom: '20px', borderBottom: '2px solid #E5E7EB' }}>
        <div>
          <h1 style={{ margin: '0', fontSize: '2.5rem', color: '#1E3A8A', letterSpacing: '-1px' }}>
            NEWS<span style={{ color: '#DC2626' }}>RADAR</span>
          </h1>
          <p style={{ margin: '5px 0 0 0', color: '#6B7280', fontSize: '1.1rem' }}>
            Ajutorul tau inteligent de Breaking News
          </p>
        </div>

        <div style={{ backgroundColor: '#FEF2F2', padding: '15px 25px', borderRadius: '8px', border: '1px solid #FECACA', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div>
            <strong style={{ display: 'block', color: '#991B1B', fontSize: '1rem' }}>🚨 Alerte Breaking News</strong>
          </div>
          <form onSubmit={handleSubscribe} style={{ display: 'flex', gap: '10px' }}>
            <input 
              type="email" 
              placeholder="Adresa ta de email..." 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              required
              style={{ padding: '8px 12px', border: '1px solid #FCA5A5', borderRadius: '4px', outline: 'none' }}
              disabled={mutationLoading} 
            />
            <button 
              type="submit" 
              style={{ 
                backgroundColor: '#DC2626', color: 'white', border: 'none', 
                padding: '8px 15px', borderRadius: '4px', fontWeight: 'bold', 
                cursor: 'pointer', opacity: mutationLoading ? 0.7 : 1 
              }}
              disabled={mutationLoading}
            >
              {mutationLoading ? 'Se trimite...' : 'Abonează-te'}
            </button>
          </form>
        </div>
      </header>
    )
}