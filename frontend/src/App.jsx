import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/catalog')
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then((data) => {
        setProducts(data.catalog || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const getPlaceholderImage = (id) => {
    return `/images/${id}.jpg`;
  };

  return (
    <>
      <header className="site-header">
        <div className="header-inner">
          <div className="logo">ByteBurst</div>
          <div className="search-bar">
            <input type="text" placeholder="Search the marketplace..." />
            <button>Go</button>
          </div>
          <div className="header-icons">
            <button className="icon-btn">♡</button>
            <button className="icon-btn">
              🛒<span className="cart-count">2</span>
            </button>
          </div>
        </div>
        <div className="chip-nav">
          <div className="chip active">All Products</div>
          <div className="chip">Best Sellers</div>
          <div className="chip">New Arrivals</div>
        </div>
      </header>

      <main className="store-container">
        <div className="store-header">
          <h1 className="glitch" data-text="ByteBurst Marketplace">ByteBurst Marketplace</h1>
          <p className="subtitle">Curated items for your lifestyle</p>
        </div>

        <div className="catalog-grid">
          {loading && <div className="status-badge">Loading live inventory...</div>}
          {error && <div className="status-badge error">Error connecting to backend: {error}</div>}

          {!loading && !error && products.length === 0 && (
            <p>No products currently available.</p>
          )}

          {!loading &&
            !error &&
            products.map((item) => (
              <div key={item.id} className="product-card">
                <div className="card-image-slider">
                  <span className="badge new">New</span>
                  <button className="wishlist-heart">♡</button>
                  <img className="slide active" src={getPlaceholderImage(item.id)} alt={item.name} />
                  <button className="quick-add-btn">+ Quick Add</button>
                </div>
                
                <div className="card-body">
                  <div className="card-header">
                    <span className="product-id">SKU #{item.id}</span>
                    <span className={`stock-pill ${item.stock < 100 ? 'low' : ''}`}>
                      {item.stock} in stock
                    </span>
                  </div>
                  <h2 className="product-title">{item.name}</h2>
                  <div className="price-row">
                    <span className="price-current">$99.00</span>
                  </div>
                  <button className="buy-button">Purchase Item</button>
                </div>
              </div>
            ))}
        </div>
        
        <div className="newsletter">
          <h3>Join our community</h3>
          <p>Get exclusive offers and botanical tips.</p>
          <form onSubmit={(e) => e.preventDefault()}>
            <input type="email" placeholder="Email address" />
            <button type="submit">Subscribe</button>
          </form>
        </div>
      </main>
    </>
  );
}

export default App;