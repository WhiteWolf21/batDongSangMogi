import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { UserPostComponent } from './user-post/user-post.component';
import { HttpClientModule } from '@angular/common/http';
import { NgxPaginationModule } from 'ngx-pagination';

@NgModule({
  declarations: [UserPostComponent],
  imports: [
    CommonModule,
    UserRoutingModule,
    HttpClientModule,
    NgxPaginationModule
  ],
  exports: [UserPostComponent]
})
export class UserModule { }
