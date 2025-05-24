import { Link } from "react-router-dom"
export default function SideBar(){
    return <>
    <nav className="w-64 h-screen bg-gray-800 text-white p-4">
      <h2 className="text-2xl font-bold mb-6">Books App</h2>
      <ul className="space-y-4">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/search">Search</Link></li>
        <li><Link to="/categories">Categories</Link></li>
      </ul>
    </nav>
    </>
}
