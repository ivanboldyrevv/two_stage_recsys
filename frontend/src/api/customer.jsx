import config from "../config"

const useCustomer = (setCustomer, randomSeed) => {
    const fetchCustomer = async () => {
            
        const params = {
            random_seed: randomSeed
        }

        const filteredParams = Object.fromEntries(
            Object.entries(params).filter(([, v]) => v !== undefined && v !== "")
        )

        const queryString = new URLSearchParams(filteredParams).toString()
        const articlesUrl = `${config.api.baseUrl}/customer/random?${queryString}`

        const response = await fetch(articlesUrl)
        const data = await response.json()

        setCustomer(data);
    }
    fetchCustomer();
}

export default useCustomer;