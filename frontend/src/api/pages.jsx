const usePages = (setPage, setTotalPages, pageNumber, pageSize, typeName, groupName) => {
    const fetchArticles = async () => {
      try {

        const params = {
          page: Number(pageNumber),
          size: Number(pageSize),
          ...(typeName && { type_name: typeName }),
          ...(groupName && { group_name: groupName.value })
        }

        const filteredParams = Object.fromEntries(
          Object.entries(params).filter(([, v]) => v !== undefined && v !== "")
        )

        const queryString = new URLSearchParams(filteredParams).toString()
        const articlesUrl = `http://localhost:5556/articles?${queryString}`

        const articlesResponse = await fetch(articlesUrl)
        if (!articlesResponse.ok) throw new Error("Articles request failed")
        
        const articlesPageData = await articlesResponse.json()

        const articlesWithImages = await Promise.all(
          articlesPageData.data.map(async article => {
            try {
              const imageUrl = `http://localhost:5556/articles/image?image_id=${article.image_id}`
              const imageResponse = await fetch(imageUrl)
              
              if (!imageResponse.ok) throw new Error("Image request failed")
              
              const imageBlob = await imageResponse.blob()
              return {
                ...article,
                imageUrl: URL.createObjectURL(imageBlob)
              }
            } catch (error) {
              console.error("Error loading image:", error)
              return { ...article, imageUrl: null }
            }
          })
        )
        
        setTotalPages(articlesPageData.total_pages);
        setPage(articlesWithImages);

      } catch (error) {
        console.error("Error fetching articles:", error)
      }
    }
    fetchArticles();
}

export default usePages