import "./App.css";

import ItemCard from "./components/ItemCard";
import ItemsContainer from "./components/ItemsContainer";
import Paginate from "./components/Paginate";
import {RecommendationSelect, ItemSelect} from "./components/Select";


const testImageUrl = 'https://image.hm.com/assets/hm/3a/74/3a7465ed33c6b9134f400343210286dae45652b5.jpg?imwidth=2160';
const testCategoryName = 'jeans';
const testItemName = 'mommy jeans';

const testItems = [
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
    <ItemCard imgUrl={testImageUrl} itemCategory={testCategoryName} itemName={testItemName} />,
];

const testOptions = [
  { value: "chocolate", label: "Chocolate" },
  { value: "strawberry", label: "Strawberry" },
  { value: "vanilla", label: "Vanilla" },
  { value: "a", label: "vb" },
  { value: "q", label: "vsd" },
  { value: "w", label: "vs" },
  { value: "e", label: "vc" },
]


const App = () => {
  const handlePageClick = () => {
    console.log("page skipped");
  }

  return (
    <div className="content">
      <div className="settings">
        <div className="navigation-container">
          <h3>Table of contents</h3>
          <a href="#">Home</a>
          <br></br>
          <a href="#">Two - stage model</a>
        </div>
        <div className="filter-container">
          <hr></hr>
          <h3>Item's filter</h3>
          <h4>Item group</h4>
          <ItemSelect
            options={testOptions}
          />
          <h4>Item type</h4>
          <ItemSelect
            options={testOptions}
          />
        </div>
        <div className="recs-filter-container">
          <hr></hr>
          <h3>Recommendation's filter</h3>
          <h4>Fetch size</h4>
          <RecommendationSelect/>
        </div>
      </div>

      <div className="items-grid">
        <div className="items-container">
          <ItemsContainer
            items={testItems}
          />
        </div>
        <div className="pagination-grid">
          <Paginate/>
        </div>
        <div className="recs-container">
          <hr></hr>
          <p>Recommendation`s</p>
          <ItemsContainer
            items={testItems}
          />
        </div>
      </div>
    </div>
  );
};

export default App;
