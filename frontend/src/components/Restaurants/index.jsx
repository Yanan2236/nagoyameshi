import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import './style.css'

const API_BASE = "http://localhost:8001";

export const Restaurants = () => {
        const [restaurants, setRestaurants] = useState([]);
        const [loading, setLoading] = useState(true);
        const [error, setError] = useState(null);

        const [name, setName] = useState('');

        const fetchRestaurants = async () => {
            setLoading(true);
            setError(null);

            const params = new URLSearchParams();
            if (name) params.append("name", name);

            const url = `${API_BASE}/api/owner/restaurants/?${params.toString()}`;
            console.log("Fetching URL:", url);

            try {
                 const res = await fetch(url);
                 if (!res.ok) {
                        throw new Error(`HTTP${res.status}`);
                 }
                 const data = await res.json();
                 setRestaurants(data.results ?? []);
            } catch (err) {
                 setError(err.message ?? "エラーが発生しました");
            } finally {
                 setLoading(false);
            }
        };

        useEffect(() => {
            fetchRestaurants();
        }, []);

        const handleSubmit = (e) => {
            e.preventDefault();
            fetchRestaurants();
        };







    return (
        <div className="restaurants">
            <form className="search-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="レストラン名で検索"
                />
                <button type="submit">検索</button>
            </form>

            {loading && <p>読み込み中...</p>}
            {error && <p>エラー: {error}</p>}

            {!loading && !error && restaurants.length === 0 && (<p>レストランが見つかりません。</p>) && (
                <ul className="restaurant-list">
                    {restaurants.map((restaurant) => (
                    <li className="restaurant-card" key={restaurant.id}>
                        <Link>
                        <h3 className="restaurant-name">{restaurant.name}</h3>
                        <p className="restaurant-genre">{restaurant.genre}</p>
                        <p className="restaurant-spot">{restaurant.spot}</p>
                        </Link>
                    </li>
                    ))}
                </ul>
            )}
        </div>
    )
}