import { Component, OnInit } from '@angular/core';
import { UserPostService } from './user-post.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-user-post',
  templateUrl: './user-post.component.html',
  styleUrls: ['./user-post.component.css']
})
export class UserPostComponent implements OnInit {

  userBuyPosts: any;
  userSellPosts: any;
  pageNum: number = 1;
  totalItem: number;
  pageSize: number = 10;

  constructor( private userPostService: UserPostService ) { }

  ngOnInit() {
    this.get();
  }

  get() {
    this.userPostService.getBuy(this.pageNum.toString()).subscribe(res => {
      console.log(res);
      this.userBuyPosts = res['userBuyPosts'];
      this.pageNum = res['currentPage'];
      this.totalItem = res['countLimit'];
      console.log(this.pageNum);
    }, error => {
      console.log(error);
    });

    this.userPostService.getSell(this.pageNum.toString()).subscribe(res => {
      console.log(res);
      this.userSellPosts = res['userSellPosts'];
      this.pageNum = res['currentPage'];
      this.totalItem = res['countLimit'];
    }, error => {
      console.log(error);
    });
  }

  onClick() {
    this.get();
  }

}