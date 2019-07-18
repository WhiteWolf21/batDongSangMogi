import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserPostService {

  private host = 'localhost';
  private port = '8080';
  private serverUrl = 'http://' + this.host + ':' + this.port;

  constructor(private http: HttpClient) { }

  getBuy(pageNum: string) {
    return this.http.get(this.serverUrl + '/api/get-user/buy/' + pageNum);
  }

  getSell(pageNum: string) {
    return this.http.get(this.serverUrl + '/api/get-user/sell/' + pageNum);
  }

}
