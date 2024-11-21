import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { AuthButtonComponent } from './authbutton.component';
import { AuthUserComponent } from './authuser.component';

@Component({
    selector: 'navigation',
    standalone: true,
    imports: [RouterOutlet, RouterModule, AuthButtonComponent, 
        AuthUserComponent],
    templateUrl: './nav.component.html'
})

export class NavComponent { }