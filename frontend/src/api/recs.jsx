import { useEffect } from "react"

const useRecs = (customerUUID, setRecsContent) => {
    const fetchArticles = async () => {
      try {

        const params = {
          customer_uuid: customerUUID
        }

        const filteredParams = Object.fromEntries(
          Object.entries(params).filter(([, v]) => v !== undefined && v !== "")
        )

        const queryString = new URLSearchParams(filteredParams).toString()
        const recsUrl = `http://localhost:5556/recs/two_stage?${queryString}`

        const response = await fetch(recsUrl)
        if (!response.ok) throw new Error("Recommendation's request failed")
        
        const recsData = await response.json()

        const detailedData = await Promise.all(
            recsData.map(async article => {
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

        setRecsContent(detailedData);

      } catch (error) {
        console.error("Error fetching articles:", error)
      }
    }

    fetchArticles()
}

export default useRecs;