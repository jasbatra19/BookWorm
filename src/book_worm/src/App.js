import {BrowserRouter as Router,Route,Routes} from 'react-router-dom'
import SideBar from './components/SideBar';
import Home from './pages/Home';
import Search from './pages/Search';
import BookDetail from './pages/BookDetail';
function App() {
  return (
    <Router>
      <div>
        <SideBar/>
        <main>
          <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path='/search' element={<Search/>}/>
            <Route path='/bookDetails' element={<BookDetail/>}/>
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
