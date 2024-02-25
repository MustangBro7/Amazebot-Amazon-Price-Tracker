import * as React from 'react';
import { useState } from 'react';
import { useEffect } from 'react';
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { data } from 'autoprefixer';


export default function InputWithButton() {
  const [textval , setTextval] = useState('')
  const [productname  , setProductname] = useState('')
  const [price , setPrice] = useState('')
  const [cards , setCards] = useState([])
  // useEffect({
    useEffect(() => {
      const fetchdata = async() =>{
      // const response = await fetch("https://amazebot.onrender.com/getdata", {  
      const response = await fetch("http://localhost:5000/getdata", {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
          })
          const data = await response.json();
      console.log(data)
      setCards(data)
      }
      fetchdata();
      checkallprice();
      console.log(cards)
    }, []);
  async function posturl(url1){
    
    const url = {url : url1}
    try{
      const response = await fetch("http://localhost:5000", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(url),
        });
      const data = await response.json();
      // cons ole.log(data)
      return data;
      // setProductname(data['Name'])
      // setPrice(data['Price'])
      // console.log(productname , price)
    }
    catch(error){
      console.log(error)
    }  
}
  function handlechange (value) {
    setTextval(value);
    console.log(value)
  }

  async function onclick(){
    console.log(textval)
    if (cards.some(obj => obj.link === textval)){
      const found = cards.findIndex(obj => obj.link === textval)
      checkprice(found)
      console.log(found)
    }
    else{
    const data = await posturl(textval)
    console.log(data['Name'])
    // setProductname(data['Name']);
    // setPrice(data['Price']);
    // src = cards['img_link']
    setCards([...cards , data])
    }
  }

  async function checkprice(value){
    console.log(value)
    const data = await posturl(cards[value]['link'])
    console.log(data)
    const new_price = data['Price']

    setCards((prevState) => {
      const updatedCards = [...prevState]; // Copy state
      // Implement price update logic (e.g., call checkprice, handle temporary changes, etc.)
      updatedCards[value].Price = new_price; // Set new price (replace with actual logic)
      return updatedCards;
    })
  }
  async function checkallprice(){
    for(let i = 0 ; i< cards.length;i++){
      checkprice(i)
    }
  }
  async function deletecard(index){
    {if (window.confirm('Are you sure you want to delete this card?')) {
      setCards(prevCards => prevCards.filter((card, i) => i !== index));}}
      console.log(cards[index]['link'])
      const del_url = {url:cards[index]['link']}
    const response = await fetch("https://amazebot.onrender.com/delete",{
      method : "DELETE",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(del_url),
    })
  }
  console.log(cards);
  return (
    <>
    <div className="flex w-full max-w-sm items-center space-x-2">
      <Input  placeholder="Enter Link" onChange={(e) =>handlechange(e.target.value)} />
      <Button type="submit" onClick={onclick}>Search</Button>
      <Button className="flex items-center justify-center" onClick={()=>checkallprice()}>Check All</Button>
     
    </div>
    {cards.map((cardcontent , index) =>(
      <Card key={index} className="lg:max-h-px-xs grid grid-cols-1 md:grid-cols-3  lg:grid-cols-4 gap-4 m-2 ">
        <img src={cardcontent['img_link']} alt={cardcontent['img_link']}  className = "p-10 w-full md:row-span-3 lg:row-span-1  object-cover max-h-px-10"></img>
        {/* <div>{cardcontent['img_link']}</div> */}
      
        <CardTitle className="flex items-center justify-center w-full p-2 md:col-span-2 lg:col-span-1"><a href={cardcontent['link']}>{cardcontent['Name']}</a></CardTitle>
        {/* <CardDescription>Card Description</CardDescription> */}
     
      
      <CardContent className="flex items-center justify-center p-2 md:col-span-2 lg:col-span-1">
        <p>{cardcontent['Price']}</p>
      </CardContent>
      <div className="flex items-center justify-center gap-2 p-2 md:col-span-2 lg:col-span-1">
      <Button className="flex items-center justify-center" onClick={()=>checkprice(index)}>Check Price</Button>
      <Button className="flex items-center justify-center" onClick={()=>deletecard(index)}>Delete</Button>
      </div>
      {/* <CardFooter>
        <p>Card Footer</p>
      </CardFooter> */}
      
    </Card>
    ))}
    
    </>
  )
}



// // posturl("https://www.amazon.in/Nike-Vision-Black-White-Sneaker-DN3577-101/dp/B09NMH8JY4/ref=sr_1_5?crid=1O7EIEUA1OKT7&keywords=nike%2Bshoes&qid=1706368305&sprefix=nike%2Bshoe%2Caps%2C375&sr=8-5&th=1&psc=1")
