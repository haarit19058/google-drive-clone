`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 07.01.2025 09:07:02
// Design Name: 
// Module Name: first_module_TB
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module first_module_TB(

    );
    reg x1, x2;
    wire f;
    
    first_module uut(
        .x1(x1),
        .x2(x2),
        .f(f)
    );
    
    initial begin
    x1 = 0; x2 = 0; #10; //delay
    x1 = 0; x2 = 1; #10;
    x1 = 1; x2 = 0; #10;
    x1 = 1; x2 = 1; #10;
    end
endmodule
