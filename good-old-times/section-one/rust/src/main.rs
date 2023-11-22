use std::{io::{self, Read}, fs::File};

fn main() {
    
}

fn touchopen(filename: String) -> io::Result<()> {
    ///

    // File::openを使用してファイルを開きます。エラーが発生した場合は、
    // ?を使用してエラーを呼び出し元に返します。
    let mut file = match File::open(&filename) {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    // ファイル内容を格納するための変数を宣言します。
    let mut contents = String::new();

    // ファイルの内容を読み込みます。エラーが発生した場合は、
    // ?を使用してエラーを呼び出し元に返します。
    match file.read_to_string(&mut contents) {
        Ok(_) => println!("File contents: \n{}", contents),
        Err(e) => return Err(e),
    };

    // 全て成功した場合、Ok(())を返します。
    Ok(())
}