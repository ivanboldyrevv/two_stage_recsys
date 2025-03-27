import React from 'react';


const ItemsContainer = ({items}) => {
    return (
        <div className="grid-container">
            {items.map((item, index) => (
                <React.Fragment key={index}>{item}</React.Fragment>
            ))}
        </div>
    );
};

export default ItemsContainer;