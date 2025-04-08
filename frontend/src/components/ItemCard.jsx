import React from "react";

const ItemCard = ({uuid, imgUrl, itemCategory, itemName, handleClick}) => {
    return (
        <div className="item-card" onClick={() => handleClick(uuid)}>
            <div className="item-image">
                <img src={imgUrl} width={120}/>
            </div>
            <div className="item-metadata">
                <p>category: {itemCategory}</p>
                <h5>{itemName}</h5>
            </div>
        </div>
    );
}

export default ItemCard;