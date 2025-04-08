import { useEffect } from "react";

const fetchArticleTypes = (setTypes) => {
    useEffect(() => {
        const fetchTypes = async () => {
            const url = "http://localhost:5556/articles/types";
            const response = await fetch(url);
            const data = await response.json();

            const types = data.map(item => ({
                value: item,
                label: item
            }))

            setTypes(types);
        }
        fetchTypes();
    }, [])
}

const fetchGroups = (setGroup) => {
    const fetchData = async () => {
        const url = "http://localhost:5556/articles/groups";
        const response = await fetch(url);
        const data = await response.json();

        const groups = data.map(item => ({
            value: item,
            label: item
        }))
        setGroup(groups);
    }
    fetchData();
}



export { fetchArticleTypes, fetchGroups };