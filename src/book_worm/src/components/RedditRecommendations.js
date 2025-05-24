import { useEffect, useState } from "react"
import { server, paths } from "../serverFile";

export default function RedditRecom(){
    const [books,setRBooks]=useState([]);
    useEffect(()=>{
        const fetchRedditRecommendations = async () => {
              try {
                const response = await fetch(`${server}${paths.redditRecommendations}`);
                console.log(response)
                const data = await response.json();
                console.log(data)
                setRBooks(data);
              } catch (err) {
                console.error("Failed to fetch new releases:", err);
              }
            };

            fetchRedditRecommendations();
    },[])
    
    return <div>
    <h2>reddit_recommendations</h2>
    <div style={{ display: "flex", overflowX: "scroll" }}>
      {books.map((book, index) => (
        <div key={index} style={{ marginRight: "20px" }}>
          <img src={book.cover} alt={book.title} width={120} />
          <p>{book.title}</p>
          <p>{book.author}</p>
        </div>
      ))}
    </div>
  </div>
}