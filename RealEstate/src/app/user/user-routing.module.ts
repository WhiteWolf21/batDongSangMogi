import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserPostComponent } from './user-post/user-post.component';

const routes: Routes = [
  {
    path: 'user-post',
    component: UserPostComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }
