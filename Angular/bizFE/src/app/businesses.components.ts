import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
    selector: 'businesses',
    standalone: true,
    imports: [RouterOutlet],
    templateUrl: './businesses.component.html',
    styleUrl: './businesses.component.css'
})
export class BusinessesComponent {
    business_list = [
        {
            "name": "Pizz Mountain",
            "town": "Coleraine",
            "rating": 5
        },
        {
            "name": "Wine Lake",
            "town": "Ballymoney",
            "rating": 3
        },
        {
            "name": "Sweet Desert",
            "town": "Ballymena",
            "rating": 4
        }
    ]
}
