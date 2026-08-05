NOTES = {
    "Artist": "One row per music artist.",

    "Album": "Albums released by an artist. Links to Artist using ArtistId.",

    "Track": "Individual songs. Links to Album using AlbumId and to Genre using GenreId. Milliseconds stores track length.",

    "Genre": "Music genres such as Rock, Jazz, Blues and Metal.",

    "MediaType": "Audio file format for each track.",

    "Playlist": "Named playlists.",

    "PlaylistTrack": "Many-to-many table linking Playlists and Tracks.",

    "Customer": "Customers who purchase music.",

    "Employee": "Employees of the music store.",

    "Invoice": "One row per customer purchase. Contains CustomerId, InvoiceDate and Total.",

    "InvoiceLine": "Each purchased track on an invoice. Links Invoice to Track and stores quantity and unit price."
}