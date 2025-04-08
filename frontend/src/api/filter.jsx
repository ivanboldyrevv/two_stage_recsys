import { useEffect } from "react";
import config from "../config";


const fetchArticleTypes = (setTypes) => {
    useEffect(() => {
        const fetchTypes = async () => {
            const url = `${config.api.baseUrl}/articles/types`;
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
        const url = `${config.api.baseUrl}/articles/groups`;
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