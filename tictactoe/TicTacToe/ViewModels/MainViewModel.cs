using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TicTacToe.ViewModels
{
    public class MainViewModel
    {
        public TicTacToeViewModel TicTacToeViewModel { get; set; }

        public MainViewModel()
        {
            TicTacToeViewModel = new TicTacToeViewModel();
        }
    }
}
