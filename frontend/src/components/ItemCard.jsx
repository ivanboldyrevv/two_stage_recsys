const testImageUrl = "https://image.hm.com/assets/hm/3a/74/3a7465ed33c6b9134f400343210286dae45652b5.jpg?imwidth=2160";
const testCategoryName = "jeans";
const testItemName = "mommy jeans";

const ItemCard = ({imgUrl, itemCategory, itemName}) => {
    const handleClick = () => {
        console.log(1);
    }

    return (
        <div className="item-card" onClick={handleClick}>
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