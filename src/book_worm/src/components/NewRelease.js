import React, { useEffect, useState } from "react";
import { server, paths } from "../serverFile";

 export default function NewRelease() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchNewReleases = async () => {
      try {
        const response = await fetch(`${server}${paths.newRelease}`);
        console.log(response)
        const data = await response.json();
        console.log(data)
        setBooks(data);
      } catch (err) {
        console.error("Failed to fetch new releases:", err);
      }
    };

    fetchNewReleases();
  }, []);

  return (
    <div>
      <h2>New Releases</h2>
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
  );
}
