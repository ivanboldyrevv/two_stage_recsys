const insertTransaction = (customerUUID, articleUUID) => {
    const fetchData = async () => {
        const url = `http://localhost:5556/transaction/${customerUUID}?article_uuid=${articleUUID}`
        const response = await fetch(url, {
            method: "POST"
        })
        const data = await response.json();
        console.log(data);
    }
    fetchData();
}


export { insertTransaction };